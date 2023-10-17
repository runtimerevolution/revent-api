from io import BytesIO

import strawberry
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from strawberry.file_uploads import Upload
from strawberry_django_plus import gql

from photo.fixtures import NO_CONTEST_FOUND, NO_SUBMISSION_FOUND
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
    AddVoteMutationResponse,
    CloseContestMutationResponse,
    CollectionType,
    ContestSubmissionType,
    ContestType,
    PictureCommentType,
    PictureType,
    UserType,
)


@strawberry.type
class Mutation:
    create_user: UserType = gql.django.create_mutation(UserInput)
    create_picture: PictureType = gql.django.create_mutation(PictureInput)
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

    @strawberry.mutation
    @transaction.atomic
    def create_picture(self, input: PictureInput, picture: Upload) -> PictureType:
        user = User.objects.get(id=input.user)

        picture_object = Picture(user=user)
        picture_object.save()
        picture_format = getattr(picture, "format")
        picture_format = picture_format.lower() if picture_format else "jpeg"

        image_bytes = BytesIO()
        picture.save(image_bytes, format=picture_format)
        image_bytes.seek(0)

        image_file = SimpleUploadedFile(
            str(picture_object.id),
            image_bytes.getvalue(),
            content_type="image/{0}".format(picture_format),
        )

        picture_object.file = image_file
        picture_object.save()

        return picture_object

    @strawberry.mutation
    def like_picture(self, user: str, picture: int) -> PictureType:
        picture = Picture.objects.get(id=picture)
        picture.likes.add(user)
        picture.save()

        return picture

    @strawberry.mutation
    def collection_add_picture(self, collection: int, picture: int) -> CollectionType:
        collection = Collection.objects.get(id=collection)
        collection.pictures.add(picture)
        collection.save()

        return collection

    @strawberry.mutation
    def contest_submission_add_vote(
        self, contestSubmission: int, user: str
    ) -> AddVoteMutationResponse:
        if submission := ContestSubmission.objects.filter(id=contestSubmission).first():
            return AddVoteMutationResponse(
                success=True, results=submission.add_vote(user), error=""
            )

        return AddVoteMutationResponse(
            success=False, results={}, error=NO_SUBMISSION_FOUND
        )

    @strawberry.mutation
    def contest_close(self, contest: int) -> CloseContestMutationResponse:
        if contest := Contest.objects.filter(id=contest).first():
            results = contest.close_contest()
            return CloseContestMutationResponse(success=True, results=results, error="")

        return CloseContestMutationResponse(
            success=False, results={}, error=NO_CONTEST_FOUND
        )
