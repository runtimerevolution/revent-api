from django.test import TestCase

from photo.schema import schema
from tests.factories import UserFactory
from tests.test_queries.query_file import user_query_all, user_query_one


class UserTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newUsers = UserFactory.create_batch(self.batch)

    def test_query_all(self):
        query = user_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), self.batch)

    def test_query_one(self):
        newUser = UserFactory.create()
        query = user_query_one

        result = schema.execute_sync(
            query,
            variable_values={"email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), 1)
        self.assertEqual(result.data["users"][0]["email"], newUser.email)
