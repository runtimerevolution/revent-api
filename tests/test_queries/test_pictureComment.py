from django.test import TestCase

from photo.schema import schema
from tests.factories import PictureCommentFactory, PictureFactory, UserFactory


class PictureCommentTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newPictures = PictureCommentFactory.create_batch(self.batch)

    def test_query_all(self):
        query = """
                    query TestQuery {
                        picture_comments {
                            user {
                                email
                            }
                            picture {
                                picture_path
                            }
                            text
                            created_at
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), self.batch)

    def test_query_one(self):
        newPictureComment = PictureCommentFactory.create()

        query = """
                    query TestQuery($id: Int!) {
                        picture_comments(id: $id) {
                            id
                            user {
                                email
                            }
                            picture {
                                picture_path
                            }
                            text
                            created_at
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"id": newPictureComment.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), 1)
        self.assertEqual(result.data["picture_comments"][0]["id"], newPictureComment.id)
        self.assertEqual(
            result.data["picture_comments"][0]["text"], newPictureComment.text
        )

    def test_query_by_user(self):
        newUser = UserFactory()
        newPictureComments = PictureCommentFactory.create_batch(3, user=newUser)

        query = """
                    query TestQuery($user_email: String!) {
                        picture_comments(user_email: $user_email) {
                            id
                            user {
                                email
                            }
                            picture {
                                picture_path
                            }
                            text
                            created_at
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["user"]["email"], newUser.email
        )
        self.assertEqual(len(result.data["picture_comments"]), len(newPictureComments))

    def test_query_by_picture(self):
        newPicture = PictureFactory()
        newPictureComments = PictureCommentFactory.create_batch(3, picture=newPicture)

        query = """
                    query TestQuery($picture_path: String!) {
                        picture_comments(picture_path: $picture_path) {
                            id
                            user {
                                email
                            }
                            picture {
                                picture_path
                            }
                            text
                            created_at
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"picture_path": newPicture.picture_path},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["picture"]["picture_path"],
            newPicture.picture_path,
        )
        self.assertEqual(len(result.data["picture_comments"]), len(newPictureComments))
