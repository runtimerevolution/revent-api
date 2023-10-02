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
    @pytest.mark.asyncio
    async def test_create(self):
        user = {
            "email": "user@user.com",
            "name_first": "Jonh",
            "name_last": "Smith",
            "user_handle": "user123",
        }

        result = await schema.execute(
            user_creation_mutation,
            variable_values={"user": user},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["create_user"], user)

    @pytest.mark.asyncio
    async def test_create_fail(self):
        user_one = {
            "email": "user@user.com",
            "name_first": "Jonh",
            "name_last": "Smith",
            "user_handle": "user123",
        }

        user_two = {
            "email": "user@user.com",
            "name_first": "Jonh2",
            "name_last": "Smith2",
            "user_handle": "user123",
        }

        result = await schema.execute(
            user_creation_mutation,
            variable_values={"user": user_one},
        )

        result_error = await schema.execute(
            mutation,
            variable_values={"user": user_two},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result_error.errors, None)
        self.assertFalse(result_error.data["create_user"]["__typename"] is None)
        self.assertEqual(
            result_error.data["create_user"]["messages"][0],
            {
                "field": "email",
                "kind": "VALIDATION",
                "message": "User with this Email already exists.",
            },
        )
        self.assertEqual(
            result_error.data["create_user"]["messages"][1],
            {
                "field": "userHandle",
                "kind": "VALIDATION",
                "message": "User with this User handle already exists.",
            },
        )

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
