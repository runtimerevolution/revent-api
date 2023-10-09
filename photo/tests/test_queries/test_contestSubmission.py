from django.test import TestCase

from photo.models import ContestSubmission
from photo.schema import schema
from photo.tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)
from photo.tests.test_queries.graphql_queries import (
    contest_submission_query_all,
    contest_submission_query_filters,
)


class ContestSubmissionTest(TestCase):
    def setUp(self):
        self.batch_size = 10
        self.contest_submissions = ContestSubmissionFactory.create_batch(
            self.batch_size
        )

    def test_query_all(self):
        result = schema.execute_sync(
            contest_submission_query_all,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_submissions"]), self.batch_size)
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

        result = schema.execute_sync(
            contest_submission_query_filters,
            variable_values={"filters": {"id": contest_submission.id}},
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

    def test_query_filters_user(self):
        user = UserFactory()
        picture = PictureFactory(user=user)
        contest_submissions = ContestSubmissionFactory.create_batch(3, picture=picture)

        result = schema.execute_sync(
            contest_submission_query_filters,
            variable_values={"filters": {"picture": {"user": {"id": str(user.id)}}}},
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

    def test_query_filters_contest(self):
        contest = ContestFactory()
        contest_submissions = ContestSubmissionFactory.create_batch(3, contest=contest)

        result = schema.execute_sync(
            contest_submission_query_filters,
            variable_values={"filters": {"contest": {"id": contest.id}}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submissions"][0]["contest"]["id"], contest.id
        )
        self.assertEqual(
            len(result.data["contest_submissions"]), len(contest_submissions)
        )
