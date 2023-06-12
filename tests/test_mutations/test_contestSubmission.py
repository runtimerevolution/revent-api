import pytest
from django.test import TestCase

from photo.schema import schema
from tests.factories import ContestFactory, PictureFactory
from tests.test_mutations.mutation_file import contest_submission_creation_mutation
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
