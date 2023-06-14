import strawberry
from django.utils import timezone
from strawberry_django_plus import gql

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

    @strawberry.mutation
    def contest_close(self, contest: int) -> ContestType:
        contest = Contest.objects.filter(id=contest).first()
        contest.active = False
        contest.voting_phase_end = timezone.now()
        contest.save()

        return contest
