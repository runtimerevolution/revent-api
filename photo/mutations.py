from io import BytesIO

import strawberry
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
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
    CollectionType,
    ContestSubmissionType,
    ContestType,
    PictureCommentType,
    PictureType,
    RessourceNotFound,
    UserType,
)


@strawberry.type
class Mutation:
    create_user: UserType = gql.django.create_mutation(UserInput)
    create_picture: PictureType = gql.django.create_mutation(PictureInput)
    create_pictureComment: PictureCommentType = gql.django.create_mutation(
        PictureCommentInput
    )
    create_collection: CollectionType = gql.django.create_mutation(CollectionInput)
    create_contest: ContestType = gql.django.create_mutation(ContestInput)
    create_contestSubmission: ContestSubmissionType = gql.django.create_mutation(
        ContestSubmissionInput
    )
    update_user: UserType = gql.django.update_mutation(UserInputPartial)
    update_picture: PictureType = gql.django.update_mutation(PictureInputPartial)
    update_pictureComment: PictureCommentType = gql.django.update_mutation(
        PictureCommentInputPartial
    )
    update_collection: CollectionType = gql.django.update_mutation(
        CollectionInputPartial
    )
    update_contest: ContestType = gql.django.update_mutation(ContestInputPartial)
    update_contestSubmission: ContestSubmissionType = gql.django.update_mutation(
        ContestSubmissionInputPartial
    )

    @strawberry.mutation
    def create_picture(self, input: PictureInput, picture: Upload) -> PictureType:
        image_bytes = BytesIO()
        picture.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        image_file = SimpleUploadedFile(
            "sample.jpg", image_bytes.getvalue(), content_type="image/jpeg"
        )

        user = User.objects.get(id=input.user)

        newPicture = Picture(user=user, file=image_file)
        newPicture.save()

        return newPicture

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
    ) -> ContestSubmissionType:
        if submission := ContestSubmission.objects.filter(id=contestSubmission):
            return submission.add_vote(user)

        return RessourceNotFound(message=NO_SUBMISSION_FOUND)

    @strawberry.mutation
    def contest_close(self, contest: int) -> ContestType:
        if contest := Contest.objects.filter(id=contest):
            return contest.close_contest()

        return RessourceNotFound(message=NO_CONTEST_FOUND)
