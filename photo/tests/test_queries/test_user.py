from django.test import TestCase

from photo.models import User
from photo.schema import schema
from photo.tests.factories import UserFactory
from photo.tests.test_queries.graphql_queries import (
    user_query_all,
    user_query_email,
    user_query_one,
)


class UserTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.new_users = UserFactory.create_batch(self.batch)

    def test_query_all(self):
        query = user_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["users"][0].keys()]),
            sorted([field.name for field in User._meta.fields]),
        )

    def test_query_one(self):
        user = UserFactory.create()
        query = user_query_one

        result = schema.execute_sync(
            query,
            variable_values={"user": str(user.id)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), 1)
        self.assertEqual(result.data["users"][0]["email"], user.email)

    def test_query_email(self):
        user = UserFactory.create()
        query = user_query_email

        result = schema.execute_sync(
            query,
            variable_values={"email": user.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), 1)
        self.assertEqual(result.data["users"][0]["id"], str(user.id))
