from io import BytesIO

import strawberry
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import DatabaseError, transaction
from django.forms import ValidationError
from strawberry.file_uploads import Upload
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
    NO_COLLECTION_FOUND,
    NO_CONTEST_FOUND,
    NO_PICTURE_FOUND,
    NO_SUBMISSION_FOUND,
    NO_USER_FOUND,
    PICTURE_SIZE_ERROR,
)
from photo.models import User

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


@strawberry.type
class Mutation:
    create_user: UserType = gql.django.create_mutation(UserInput)
    create_picture_comment: PictureCommentType = gql.django.create_mutation(
        PictureCommentInput
    )
    create_collection: CollectionType = gql.django.create_mutation(CollectionInput)
    create_contest: ContestType = gql.django.create_mutation(ContestInput)
    create_contest_submission: ContestSubmissionType = gql.django.create_mutation(
        ContestSubmissionInput
    )
    update_user: UserType = gql.django.update_mutation(UserInputPartial)
    update_picture: PictureType = gql.django.update_mutation(PictureInputPartial)
    update_picture_comment: PictureCommentType = gql.django.update_mutation(
        PictureCommentInputPartial
    )
    update_collection: CollectionType = gql.django.update_mutation(
        CollectionInputPartial
    )
    update_contest: ContestType = gql.django.update_mutation(ContestInputPartial)
    update_contest_submission: ContestSubmissionType = gql.django.update_mutation(
        ContestSubmissionInputPartial
    )
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
    def create_picture(
        self, input: PictureInput, picture: Upload
    ) -> CreatePictureMutationResponse:
        try:
            with transaction.atomic():
                if not (user := User.objects.filter(id=input.user).first()):
                    raise ValidationError(message=NO_USER_FOUND)

                picture_object = Picture(user=user)
                picture_object.save()

                image_bytes = BytesIO()
                picture.save(image_bytes, format="webp")
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

    @strawberry.mutation
    def contest_submission_add_vote(
        self, contestSubmission: int, user: str
    ) -> AddVoteMutationResponse:
        if submission := ContestSubmission.objects.filter(id=contestSubmission).first():
            return AddVoteMutationResponse(
                success=True, results=submission.add_vote(user), errors=""
            )

        return AddVoteMutationResponse(
            success=False, results={}, errors=NO_SUBMISSION_FOUND
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
