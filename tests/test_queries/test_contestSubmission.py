from django.test import TestCase

from photo.schema import schema
from tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)
from tests.test_queries.query_file import (
    contest_submission_query_all,
    contest_submission_query_contest,
    contest_submission_query_one,
    contest_submission_query_user,
)


class ContestSubmissionTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newContestSubmissions = ContestSubmissionFactory.create_batch(self.batch)

    def test_query_all(self):
        query = contest_submission_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_submissions"]), self.batch)

    def test_query_one(self):
        newContestSubmission = ContestSubmissionFactory.create()

        query = contest_submission_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": newContestSubmission.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_submissions"]), 1)
        self.assertEqual(
            result.data["contest_submissions"][0]["id"], newContestSubmission.id
        )
        self.assertEqual(
            result.data["contest_submissions"][0]["picture"]["picture_path"],
            newContestSubmission.picture.picture_path,
        )

    def test_query_by_user(self):
        newUser = UserFactory()
        newPicture = PictureFactory(user=newUser)
        newContestSubmissions = ContestSubmissionFactory.create_batch(
            3, picture=newPicture
        )

        query = contest_submission_query_user

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submissions"][0]["picture"]["user"]["email"],
            newUser.email,
        )
        self.assertEqual(
            len(result.data["contest_submissions"]), len(newContestSubmissions)
        )

    def test_query_by_contest(self):
        newContest = ContestFactory()
        newContestSubmissions = ContestSubmissionFactory.create_batch(
            3, contest=newContest
        )

        query = contest_submission_query_contest

        result = schema.execute_sync(
            query,
            variable_values={"contest": newContest.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submissions"][0]["contest"]["id"], newContest.id
        )
        self.assertEqual(
            len(result.data["contest_submissions"]), len(newContestSubmissions)
        )
