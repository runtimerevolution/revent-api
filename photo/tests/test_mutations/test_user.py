import pytest
from django.test import TestCase
from django.utils import timezone

from photo.schema import schema
from photo.tests.factories import PictureFactory, UserFactory
from .graphql_mutations import (
    user_creation_mutation,
    user_update_mutation,
)


class UserTest(TestCase):
    def test_update(self):
        update_profile_picture_time = timezone.now()
        user = UserFactory(profile_picture_updated_at=update_profile_picture_time)
        picture = PictureFactory(user=user)
        updatedUser = {
            "pk": str(user.id),
            "email": user.email,
            "name_first": "John",
            "name_last": "Smith",
            "profile_picture": picture.id,
            "user_handle": "johnSmithHandle",
        }

        result = schema.execute_sync(
            user_update_mutation,
            variable_values={
                "user": updatedUser,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["update_user"]["email"], user.email)
        self.assertEqual(
            result.data["update_user"]["name_first"], updatedUser["name_first"]
        )
        self.assertEqual(
            result.data["update_user"]["name_last"], updatedUser["name_last"]
        )
        self.assertEqual(
            result.data["update_user"]["profile_picture"]["id"],
            updatedUser["profile_picture"],
        )
        self.assertEqual(
            result.data["update_user"]["user_handle"], updatedUser["user_handle"]
        )
        self.assertFalse(
            result.data["update_user"]["profile_picture_updated_at"]
            == str(update_profile_picture_time).replace(" ", "T")
        )

    def test_update_profile_picture_updated_at(self):
        update_profile_picture_time = timezone.now()
        user = UserFactory(profile_picture_updated_at=update_profile_picture_time)
        updated_user = {
            "pk": str(user.id),
            "email": user.email,
            "name_first": "Test1",
            "name_last": "Test2",
            "profile_picture": user.profile_picture.id,
            "user_handle": "Test123",
        }

        result = schema.execute_sync(
            user_update_mutation,
            variable_values={
                "user": updated_user,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_user"]["profile_picture_updated_at"],
            str(update_profile_picture_time).replace(" ", "T"),
        )
