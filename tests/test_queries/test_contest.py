from django.test import TestCase

from photo.schema import schema
from tests.factories import ContestFactory, UserFactory


class ContestTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newContests = ContestFactory.create_batch(self.batch)

    def test_query_all(self):
        query = """
                    query TestQuery {
                        contests {
                            id
                            title
                            description
                            created_by {
                                email
                            }
                            cover_picture {
                                picture_path
                            }
                            prize
                            automated_dates
                            upload_phase_start
                            upload_phase_end
                            voting_phase_end
                            active
                            winners {
                                email
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), self.batch)

    def test_query_one(self):
        newContest = ContestFactory.create()

        query = """
                    query TestQuery($id: Int!) {
                        contests(id: $id) {
                            id
                            title
                            description
                            created_by {
                                email
                            }
                            cover_picture {
                                picture_path
                            }
                            prize
                            automated_dates
                            upload_phase_start
                            upload_phase_end
                            voting_phase_end
                            active
                            winners {
                                email
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"id": newContest.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 1)
        self.assertEqual(result.data["contests"][0]["id"], newContest.id)

    def test_query_by_user(self):
        newUser = UserFactory()
        newContests = ContestFactory.create_batch(3, created_by=newUser)

        query = """
                    query TestQuery($user_email: String!) {
                        contests(user_email: $user_email) {
                            id
                            title
                            description
                            created_by {
                                email
                            }
                            cover_picture {
                                picture_path
                            }
                            prize
                            automated_dates
                            upload_phase_start
                            upload_phase_end
                            voting_phase_end
                            active
                            winners {
                                email
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), len(newContests))
        self.assertEqual(
            result.data["contests"][0]["created_by"]["email"], newUser.email
        )
