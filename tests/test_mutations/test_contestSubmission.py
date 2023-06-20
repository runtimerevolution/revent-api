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
from tests.test_queries.query_file import contest_query_one, picture_query_one


class ContestSubmissionTest(TestCase):
    def setUp(self):
        newPicture = PictureFactory()
        newContest = ContestFactory()

        newPictureResult = schema.execute_sync(
            picture_query_one,
            variable_values={"picture_path": newPicture.picture_path},
        )
        newContestResult = schema.execute_sync(
            contest_query_one,
            variable_values={"id": newContest.id},
        )

        self.newPicture = newPictureResult.data["pictures"][0]
        self.newContest = newContestResult.data["contests"][0]

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = contest_submission_creation_mutation
        newPicture = self.newPicture
        newContest = self.newContest

        newContestSubmission = {
            "picture": newPicture["picture_path"],
            "contest": newContest["id"],
        }

        result = await schema.execute(
            mutation,
            variable_values={"contestSubmission": newContestSubmission},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_contestSubmission"]["picture"]["user"]["email"],
            newPicture["user"]["email"],
        )
        self.assertEqual(
            result.data["create_contestSubmission"]["picture"]["picture_path"],
            newPicture["picture_path"],
        )
        self.assertEqual(
            result.data["create_contestSubmission"]["contest"]["id"], newContest["id"]
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
            "picture": newPicture.picture_path,
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
            result.data["update_contestSubmission"]["picture"]["picture_path"],
            updatedContestSubmission["picture"],
        )
        self.assertEqual(
            result.data["update_contestSubmission"]["submission_date"],
            str(updatedContestSubmission["submission_date"]).replace(" ", "T"),
        )
