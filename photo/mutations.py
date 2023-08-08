import strawberry
from django.utils import timezone
from strawberry.file_uploads import Upload
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

    def create_picture(self, input: PictureInput, picture: Upload) -> PictureType:
        return Picture(user=input.user, picture_path=picture)

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
        contestSubmission = ContestSubmission.objects.get(id=contestSubmission)
        contestSubmission.votes.add(user)
        contestSubmission.save()

        return contestSubmission

    @strawberry.mutation
    def contest_close(self, contest: int) -> ContestType:
        contest = Contest.objects.get(id=contest)
        contest.voting_phase_end = timezone.now()
        contest.status = "closed"
        contest.save()

        return contest
