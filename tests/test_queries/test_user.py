from django.test import TestCase

from photo.schema import schema
from tests.factories import UserFactory


class UserTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newUsers = UserFactory.create_batch(self.batch)

    def test_query_all(self):
        query = """
                    query TestQuery {
                        users {
                            email
                            name_first
                            name_last
                            profile_picture {
                                picture_path
                            }
                            profile_picture_updated_at
                            user_handle
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), self.batch)

    def test_query_one(self):
        newUser = UserFactory.create()
        query = """
                    query TestQuery($email: String!) {
                        users(email: $email) {
                            email
                            name_first
                            name_last
                            profile_picture {
                                picture_path
                            }
                            profile_picture_updated_at
                            user_handle
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["users"]), 1)
        self.assertEqual(result.data["users"][0]["email"], newUser.email)
