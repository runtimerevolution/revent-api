from django.test import TestCase

from photo.models import Picture
from photo.schema import schema
from photo.tests.factories import PictureFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    picture_query_all,
    picture_query_one,
)


class PictureTest(TestCase):
    def setUp(self):
        self.batch = 10
        user = UserFactory(user_profile_picture=True)
        self.new_pictures = PictureFactory.create_batch(
            self.batch,
            user=user,
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
        likes_users = UserFactory.create_batch(3, user_profile_picture=True)
        user = UserFactory(user_profile_picture=True)
        picture = PictureFactory.create(user=user, user_likes=likes_users)
        query = picture_query_one

        result = schema.execute_sync(
            query,
            variable_values={"picture": picture.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["pictures"]), 1)
        self.assertEqual(result.data["pictures"][0]["id"], picture.id)
        self.assertEqual(result.data["pictures"][0]["file"], picture.file)
        self.assertEqual(len(result.data["pictures"][0]["likes"]), len(likes_users))
