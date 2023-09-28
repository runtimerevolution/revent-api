from django.test import TestCase

from photo.models import ContestSubmission
from photo.schema import schema
from photo.tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)
from photo.tests.test_queries.query_file import (
    contest_submission_query_all,
    contest_submission_query_contest,
    contest_submission_query_one,
    contest_submission_query_user,
)


class ContestSubmissionTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.contest_submissions = ContestSubmissionFactory.create_batch(self.batch)

    def test_query_all(self):
        query = contest_submission_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_submissions"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["contest_submissions"][0].keys()]),
            sorted(
                [
                    field.name
                    for field in (
                        ContestSubmission._meta.fields
                        + ContestSubmission._meta.many_to_many
                    )
                ]
            ),
        )

    def test_query_one(self):
        contest_submission = ContestSubmissionFactory.create()

        query = contest_submission_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": contest_submission.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_submissions"]), 1)
        self.assertEqual(
            result.data["contest_submissions"][0]["id"], contest_submission.id
        )
        self.assertEqual(
            result.data["contest_submissions"][0]["picture"]["id"],
            contest_submission.picture.id,
        )

    def test_query_by_user(self):
        user = UserFactory()
        picture = PictureFactory(user=user)
        contest_submissions = ContestSubmissionFactory.create_batch(3, picture=picture)

        query = contest_submission_query_user

        result = schema.execute_sync(
            query,
            variable_values={"user": str(user.id)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submissions"][0]["picture"]["id"],
            picture.id,
        )
        self.assertEqual(
            result.data["contest_submissions"][0]["picture"]["user"]["id"],
            str(user.id),
        )
        self.assertEqual(
            len(result.data["contest_submissions"]), len(contest_submissions)
        )

    def test_query_by_contest(self):
        contest = ContestFactory()
        contest_submissions = ContestSubmissionFactory.create_batch(3, contest=contest)

        query = contest_submission_query_contest

        result = schema.execute_sync(
            query,
            variable_values={"contest": contest.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submissions"][0]["contest"]["id"], contest.id
        )
        self.assertEqual(
            len(result.data["contest_submissions"]), len(contest_submissions)
        )
