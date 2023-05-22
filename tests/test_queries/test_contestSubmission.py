from django.test import TestCase

from photo.schema import schema
from tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)


class ContestSubmissionTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newContestSubmissions = ContestSubmissionFactory.create_batch(self.batch)

    def test_query_all(self):
        query = """
                    query TestQuery {
                        contest_submissions {
                            id
                            contest {
                                id
                            }
                            picture {
                                picture_path
                                user {
                                    email
                                }
                            }
                            submission_date
                            votes {
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
        self.assertEqual(len(result.data["contest_submissions"]), self.batch)

    def test_query_one(self):
        newContestSubmission = ContestSubmissionFactory.create()

        query = """
                    query TestQuery($id: Int!) {
                        contest_submissions(id: $id) {
                            id
                            contest {
                                id
                            }
                            picture {
                                picture_path
                                user {
                                    email
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """

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

        query = """
                    query TestQuery($user_email: String!) {
                        contest_submissions(user_email: $user_email) {
                            id
                            contest {
                                id
                            }
                            picture {
                                picture_path
                                user {
                                    email
                                }
                            }
                            submission_date
                            votes {
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

        query = """
                    query TestQuery($contest: Int!) {
                        contest_submissions(contest: $contest) {
                            id
                            contest {
                                id
                            }
                            picture {
                                picture_path
                                user {
                                    email
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """

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
