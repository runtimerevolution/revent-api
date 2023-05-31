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
