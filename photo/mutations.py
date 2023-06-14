import strawberry
from strawberry_django_plus import gql

from .inputs import (
    CollectionInput,
    ContestInput,
    ContestSubmissionInput,
    PictureCommentInput,
    PictureInput,
    UserInput,
)
from .models import Collection, ContestSubmission, Picture
from .types import (
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
    create_pictureComment: PictureCommentType = gql.django.create_mutation(
        PictureCommentInput
    )
    create_collection: CollectionType = gql.django.create_mutation(CollectionInput)
    create_contest: ContestType = gql.django.create_mutation(ContestInput)
    create_contestSubmission: ContestSubmissionType = gql.django.create_mutation(
        ContestSubmissionInput
    )

    @strawberry.mutation
    def like_picture(self, user: str, picture: str) -> PictureType:
        picture = Picture.objects.filter(picture_path=picture).first()
        picture.likes.add(user)
        picture.save()

        return picture

    @strawberry.mutation
    def collection_add_picture(self, collection: int, picture: str) -> CollectionType:
        collection = Collection.objects.filter(id=collection).first()
        collection.pictures.add(picture)
        collection.save()

        return collection

    @strawberry.mutation
    def contest_submission_add_vote(
        self, contestSubmission: int, user: str
    ) -> ContestSubmissionType:
        contestSubmission = ContestSubmission.objects.filter(
            id=contestSubmission
        ).first()
        contestSubmission.votes.add(user)
        contestSubmission.save()

        return contestSubmission
