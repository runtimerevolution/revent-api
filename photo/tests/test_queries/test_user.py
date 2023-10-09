from django.test import TestCase

from photo.schema import schema
from photo.tests.factories import UserFactory
from photo.tests.test_queries.graphql_queries import user_query_one


class UserTest(TestCase):
    def setUp(self):
        self.batch_size = 10
        self.new_users = UserFactory.create_batch(self.batch_size)

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
