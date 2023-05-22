from django.test import TestCase

from photo.schema import schema
from tests.factories import PictureFactory, UserFactory


class PictureTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newPictures = PictureFactory.create_batch(
            self.batch,
            user=UserFactory(user_profile_picture=True),
            user_likes=UserFactory.create_batch(2, user_profile_picture=True),
        )

    def test_query_all(self):
        query = """
                    query TestQuery {
                        pictures {
                            user {
                                email
                                name_first
                                name_last
                            }
                            picture_path
                            likes {
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
        self.assertEqual(len(result.data["pictures"]), self.batch)
        self.assertEqual(len(result.data["pictures"][0]["likes"]), 2)

    def test_query_one(self):
        newLikesUsers = UserFactory.create_batch(3, user_profile_picture=True)
        newPicture = PictureFactory.create(
            user=UserFactory(user_profile_picture=True), user_likes=newLikesUsers
        )
        query = """
                    query TestQuery($picture_path: String!) {
                        pictures(picture_path: $picture_path) {
                            user {
                                email
                                name_first
                                name_last
                            }
                            picture_path
                            likes {
                                email
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"picture_path": newPicture.picture_path},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["pictures"]), 1)
        self.assertEqual(
            result.data["pictures"][0]["picture_path"], newPicture.picture_path
        )
        self.assertEqual(len(result.data["pictures"][0]["likes"]), len(newLikesUsers))
