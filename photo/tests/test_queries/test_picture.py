from django.test import TestCase

from photo.models import Picture
from photo.schema import schema
from photo.tests.factories import PictureFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    picture_query_all,
    picture_query_filters,
)


class PictureTest(TestCase):
    def setUp(self):
        self.batch_size = 10
        user = UserFactory(user_profile_picture=True)
        self.new_pictures = PictureFactory.create_batch(
            self.batch_size,
            user=user,
            user_likes=UserFactory.create_batch(2, user_profile_picture=True),
        )

    def test_query_all(self):
        result = schema.execute_sync(
            picture_query_all,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["pictures"]), self.batch_size)
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

    def test_query_filters_id(self):
        likes_users = UserFactory.create_batch(3, user_profile_picture=True)
        user = UserFactory(user_profile_picture=True)
        picture = PictureFactory.create(user=user, user_likes=likes_users)

        result = schema.execute_sync(
            picture_query_filters,
            variable_values={"filters": {"id": picture.id}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["pictures"]), 1)
        self.assertEqual(result.data["pictures"][0]["id"], picture.id)
        self.assertEqual(result.data["pictures"][0]["file"], picture.file)
        self.assertEqual(len(result.data["pictures"][0]["likes"]), len(likes_users))

    def test_query_filters_user(self):
        number_pictures = 5
        user = UserFactory(user_profile_picture=True)
        PictureFactory.create_batch(number_pictures, user=user)

        result = schema.execute_sync(
            picture_query_filters,
            variable_values={"filters": {"user": {"id": str(user.id)}}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["pictures"]), number_pictures)
        self.assertEqual(result.data["pictures"][0]["user"]["id"], str(user.id))
