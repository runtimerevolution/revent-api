from django.test import TestCase

from photo.models import Picture
from photo.schema import schema
from tests.factories import PictureFactory, UserFactory
from tests.test_queries.query_file import picture_query_all, picture_query_one


class PictureTest(TestCase):
    def setUp(self):
        self.batch = 10
        newUser = UserFactory(user_profile_picture=True)
        self.newPictures = PictureFactory.create_batch(
            self.batch,
            user=newUser,
            user_likes=UserFactory.create_batch(2, user_profile_picture=True),
        )

    def test_query_all(self):
        query = picture_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["pictures"]), self.batch)
        self.assertEqual(len(result.data["pictures"][0]["likes"]), 2)
        self.assertEqual(
            sorted([key for key in result.data["pictures"][0].keys()]),
            sorted(
                [
                    field.name
                    for field in (Picture._meta.fields + Picture._meta.many_to_many)
                ]
            ),
        )

    def test_query_one(self):
        newLikesUsers = UserFactory.create_batch(3, user_profile_picture=True)
        newUser = UserFactory(user_profile_picture=True)
        newPicture = PictureFactory.create(user=newUser, user_likes=newLikesUsers)
        query = picture_query_one

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
