from django.test import TestCase

from photo.models import Contest
from photo.schema import schema
from tests.factories import ContestFactory, UserFactory
from tests.test_queries.query_file import (
    contest_query_all,
    contest_query_creator,
    contest_query_one,
)


class ContestTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newContests = ContestFactory.create_batch(self.batch)

    def test_query_all(self):
        query = contest_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["contests"][0].keys()]),
            sorted(
                [
                    field.name
                    for field in (Contest._meta.fields + Contest._meta.many_to_many)
                ]
            ),
        )

    def test_query_one(self):
        newContest = ContestFactory.create()

        query = contest_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": newContest.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 1)
        self.assertEqual(result.data["contests"][0]["id"], newContest.id)

    def test_query_by_creator(self):
        newUser = UserFactory()
        newContests = ContestFactory.create_batch(3, created_by=newUser)

        query = contest_query_creator

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), len(newContests))
        self.assertEqual(
            result.data["contests"][0]["created_by"]["email"], newUser.email
        )
