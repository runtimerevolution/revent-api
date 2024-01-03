from io import BytesIO

import strawberry
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import DatabaseError, transaction
from django.forms import ValidationError
from strawberry_django_plus import gql

from photo.filters import (
    CollectionFilter,
    ContestFilter,
    ContestSubmissionFilter,
    PictureCommentFilter,
    PictureFilter,
    UserFilter,
)
from photo.fixtures import (
    CREATE_PICTURE_ERROR,
    CREATE_PICTURE_SUBMISSION_ERROR,
    NO_COLLECTION_FOUND,
    NO_CONTEST_FOUND,
    NO_PICTURE_FOUND,
    NO_SUBMISSION_FOUND,
    NO_USER_FOUND,
    PICTURE_SIZE_ERROR,
)
from photo.models import User
from photo.permissions import IsAuthenticated
from photo.queries import Info

from .inputs import (
    CollectionInput,
    CollectionInputPartial,
    ContestInput,
    ContestInputPartial,
    ContestSubmissionInput,
    ContestSubmissionInputPartial,
    PictureCommentInput,
    PictureCommentInputPartial,
    PictureInput,
    PictureInputPartial,
    UserInput,
    UserInputPartial,
)
from .models import Collection, Contest, ContestSubmission, Picture
from .types import (
    AddLikeMutationResponse,
    AddVoteMutationResponse,
    CloseContestMutationResponse,
    CollectionAddPictureMutationResponse,
    CollectionType,
    ContestSubmissionType,
    ContestType,
    CreateContestSubmissiomMutationResponse,
    CreatePictureMutationResponse,
    PictureCommentType,
    PictureType,
    UserType,
)


def try_catch(function):
    def wrapper():
        print("Something is happening before the function is called.")
        try:
            return function()
        except Exception as e:
            print(e)
        print("Something is happening after the function is called.")

    return wrapper


class PictureError(Exception):
    def __init__(self, message) -> None:
        super().__init__()
        self.message = message


class NotFoundError(Exception):
    def __init__(self, message) -> None:
        super().__init__()
        self.message = message


def picture_creation(input: PictureInput) -> CreatePictureMutationResponse:
    try:
        with transaction.atomic():
            if not (user := User.objects.filter(id=input.user).first()):
                raise ValidationError(message=NO_USER_FOUND)

            picture_object = Picture(user=user)
            picture_object.save()

            image_bytes = BytesIO()
            input.file.save(image_bytes, format="webp")
            if image_bytes.tell() > int(settings.MAX_PICTURE_SIZE):
                raise ValidationError(message=PICTURE_SIZE_ERROR)
            image_bytes.seek(0)

            image_file = SimpleUploadedFile(
                str(picture_object.id),
                image_bytes.getvalue(),
                content_type="image/webp",
            )

            picture_object.file = image_file
            picture_object.save()

            return CreatePictureMutationResponse(
                success=True, results=picture_object, errors=""
            )
    except ValidationError as e:
        return CreatePictureMutationResponse(
            success=False, results={}, errors=e.message
        )
    except DatabaseError:
        return CreatePictureMutationResponse(
            success=False, results={}, errors=CREATE_PICTURE_ERROR
        )


@strawberry.type
class Mutation:
    create_user: UserType = gql.django.create_mutation(UserInput)
    create_picture_comment: PictureCommentType = gql.django.create_mutation(
        PictureCommentInput
    )
    create_collection: CollectionType = gql.django.create_mutation(CollectionInput)
    create_contest: ContestType = gql.django.create_mutation(ContestInput)
    update_user: UserType = gql.django.update_mutation(UserInputPartial)
    update_picture: PictureType = gql.django.update_mutation(PictureInputPartial)
    update_picture_comment: PictureCommentType = gql.django.update_mutation(
        PictureCommentInputPartial
    )
    update_collection: CollectionType = gql.django.update_mutation(
        CollectionInputPartial
    )
    update_contest: ContestType = gql.django.update_mutation(ContestInputPartial)
    delete_user: UserType = gql.django.delete_mutation(UserFilter)
    delete_picture: PictureType = gql.django.delete_mutation(PictureFilter)
    delete_picture_comment: PictureCommentType = gql.django.delete_mutation(
        PictureCommentFilter
    )
    delete_collection: CollectionType = gql.django.delete_mutation(CollectionFilter)
    delete_contest: ContestType = gql.django.delete_mutation(ContestFilter)
    delete_contest_submission: ContestSubmissionType = gql.django.delete_mutation(
        ContestSubmissionFilter
    )

    @strawberry.mutation
    def create_picture(self, input: PictureInput) -> CreatePictureMutationResponse:
        return picture_creation(input=input)

    @strawberry.mutation
    def create_contest_submission(
        self, input: ContestSubmissionInput
    ) -> CreateContestSubmissiomMutationResponse:
        try:
            with transaction.atomic():
                picture_response = picture_creation(input=input.picture)
                if not picture_response.success:
                    raise PictureError(picture_response.errors)
                if not (contest := Contest.objects.filter(id=input.contest).first()):
                    raise NotFoundError(NO_CONTEST_FOUND)
                if not (
                    picture := Picture.objects.filter(
                        id=picture_response.results.id
                    ).first()
                ):
                    raise NotFoundError(NO_PICTURE_FOUND)
                contest_submission = ContestSubmission(contest=contest, picture=picture)
                contest_submission.save()

                return CreateContestSubmissiomMutationResponse(
                    success=True, results=contest_submission, errors=""
                )
        except PictureError as e:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=e.message
            )
        except NotFoundError as e:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=e.message
            )
        except ValidationError as e:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=e.message
            )
        except DatabaseError:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=CREATE_PICTURE_SUBMISSION_ERROR
            )

    @strawberry.mutation
    def update_contest_submission(
        self, input: ContestSubmissionInputPartial
    ) -> CreateContestSubmissiomMutationResponse:
        try:
            with transaction.atomic():
                if not (
                    contest_submission := ContestSubmission.objects.filter(
                        id=input.id
                    ).first()
                ):
                    raise NotFoundError(NO_SUBMISSION_FOUND)
                old_picture = contest_submission.picture

                picture_response = picture_creation(input=input.picture)
                if not picture_response.success:
                    raise PictureError(picture_response.errors)

                if not (
                    picture := Picture.objects.filter(
                        id=picture_response.results.id
                    ).first()
                ):
                    raise NotFoundError(NO_PICTURE_FOUND)

                contest_submission.picture = picture
                contest_submission.save()

                old_picture.delete()

                return CreateContestSubmissiomMutationResponse(
                    success=True, results=contest_submission, errors=""
                )

        except NotFoundError as e:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=e.message
            )
        except ValidationError as e:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=e.message
            )
        except DatabaseError:
            return CreateContestSubmissiomMutationResponse(
                success=False, results={}, errors=CREATE_PICTURE_SUBMISSION_ERROR
            )

    @strawberry.mutation
    def like_picture(self, picture: int, user: str) -> AddLikeMutationResponse:
        if picture := Picture.objects.filter(id=picture).first():
            return AddLikeMutationResponse(
                success=True, results=picture.like_picture(user), errors=""
            )

        return AddLikeMutationResponse(
            success=False, results={}, errors=NO_PICTURE_FOUND
        )

    @strawberry.mutation
    def collection_add_picture(
        self, collection: int, picture: int
    ) -> CollectionAddPictureMutationResponse:
        if collection := Collection.objects.filter(id=collection).first():
            return CollectionAddPictureMutationResponse(
                success=True, results=collection.add_picture(picture), errors=""
            )

        return CollectionAddPictureMutationResponse(
            success=False, results={}, errors=NO_COLLECTION_FOUND
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def contest_submission_add_vote(
        self, info: Info, contestSubmission: int, user: str
    ) -> AddVoteMutationResponse | None:
        try:
            submission = ContestSubmission.objects.filter(id=contestSubmission).first()
            if not submission:
                return AddVoteMutationResponse(
                    success=False, results=None, errors=NO_SUBMISSION_FOUND
                )

            return AddVoteMutationResponse(
                success=True, results=submission.add_vote(user), errors=""
            )

        except Exception as e:
            return AddVoteMutationResponse(
                success=False, results=None, errors=e.message
            )

    @strawberry.mutation
    def contest_close(self, contest: int) -> CloseContestMutationResponse:
        if contest := Contest.objects.filter(id=contest).first():
            results = contest.close_contest()
            return CloseContestMutationResponse(
                success=True, results=results, errors=""
            )

        return CloseContestMutationResponse(
            success=False, results={}, errors=NO_CONTEST_FOUND
        )
