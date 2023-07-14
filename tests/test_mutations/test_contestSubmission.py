import pytest
from django.test import TestCase
from django.utils import timezone

from photo.schema import schema
from tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)
from tests.test_mutations.mutation_file import (
    contest_submission_creation_mutation,
    contest_submission_update_mutation,
    contest_submission_vote_mutation,
)


class ContestSubmissionTest(TestCase):
    def setUp(self):
        self.newPicture = PictureFactory()
        self.newContest = ContestFactory()

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = contest_submission_creation_mutation
        newPicture = self.newPicture
        newContest = self.newContest

        newContestSubmission = {
            "picture": newPicture.id,
            "contest": newContest.id,
        }

        result = await schema.execute(
            mutation,
            variable_values={"contestSubmission": newContestSubmission},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_contestSubmission"]["picture"]["user"]["email"],
            newPicture.user.email,
        )
        self.assertEqual(
            result.data["create_contestSubmission"]["picture"]["id"],
            newPicture.id,
        )
        self.assertEqual(
            result.data["create_contestSubmission"]["contest"]["id"], newContest.id
        )

    def test_vote(self):
        mutation = contest_submission_vote_mutation

        newContestSubmission = ContestSubmissionFactory()
        newUserVote = UserFactory()

        result = schema.execute_sync(
            mutation,
            variable_values={
                "contestSubmission": newContestSubmission.id,
                "user": newUserVote.email,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submission_add_vote"]["votes"][0]["email"],
            newUserVote.email,
        )

    def test_update(self):
        mutation = contest_submission_update_mutation

        newContest = ContestFactory()

        newUser = UserFactory()
        originalPicture = PictureFactory(user=newUser, picture_path="www.original.com")
        newContestSubmission = ContestSubmissionFactory(
            contest=newContest, picture=originalPicture
        )

        self.assertEqual(
            newContestSubmission.picture.picture_path, originalPicture.picture_path
        )

        newPicture = PictureFactory(user=newUser, picture_path="www.test.com")

        updatedContestSubmission = {
            "id": newContestSubmission.id,
            "picture": newPicture.id,
            "submission_date": str(timezone.now()),
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "contestSubmission": updatedContestSubmission,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_contestSubmission"]["picture"]["id"],
            updatedContestSubmission["picture"],
        )
        self.assertEqual(
            result.data["update_contestSubmission"]["submission_date"],
            str(updatedContestSubmission["submission_date"]).replace(" ", "T"),
        )
