import pytest
from django.test import TestCase
from django.utils import timezone
from tests.factories import PictureFactory, UserFactory
from tests.test_mutations.mutation_file import (
    user_creation_mutation,
    user_update_mutation,
)

from photo.schema import schema


class UserTest(TestCase):
    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = user_creation_mutation
        newUser = {
            "email": "user@user.com",
            "name_first": "Jonh",
            "name_last": "Smith",
            "user_handle": "user123",
        }

        result = await schema.execute(
            mutation,
            variable_values={"user": newUser},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["create_user"], newUser)

    @pytest.mark.asyncio
    async def test_create_fail(self):
        mutation = user_creation_mutation
        newUser = {
            "email": "user@user.com",
            "name_first": "Jonh",
            "name_last": "Smith",
            "user_handle": "user123",
        }

        newUser2 = {
            "email": "user@user.com",
            "name_first": "Jonh2",
            "name_last": "Smith2",
            "user_handle": "user123",
        }

        result = await schema.execute(
            mutation,
            variable_values={"user": newUser},
        )

        resultError = await schema.execute(
            mutation,
            variable_values={"user": newUser2},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(resultError.errors, None)
        self.assertFalse(resultError.data["create_user"]["__typename"] is None)
        self.assertEqual(
            resultError.data["create_user"]["messages"][0],
            {
                "field": "email",
                "kind": "VALIDATION",
                "message": "User with this Email already exists.",
            },
        )
        self.assertEqual(
            resultError.data["create_user"]["messages"][1],
            {
                "field": "userHandle",
                "kind": "VALIDATION",
                "message": "User with this User handle already exists.",
            },
        )

    def test_update(self):
        mutation = user_update_mutation

        updatedProfilePictureTime = timezone.now()
        newUser = UserFactory(profile_picture_updated_at=updatedProfilePictureTime)
        newPicture = PictureFactory(user=newUser)
        updatedUser = {
            "pk": newUser.email,
            "name_first": "John",
            "name_last": "Smith",
            "profile_picture": newPicture.id,
            "user_handle": "johnSmithHandle",
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "user": updatedUser,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["update_user"]["email"], newUser.email)
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
            == str(updatedProfilePictureTime).replace(" ", "T")
        )

    def test_update_profile_picture_updated_at(self):
        mutation = user_update_mutation

        updatedProfilePictureTime = timezone.now()
        newUser = UserFactory(profile_picture_updated_at=updatedProfilePictureTime)
        updatedUser = {
            "pk": newUser.email,
            "name_first": "Test1",
            "name_last": "Test2",
            "profile_picture": newUser.profile_picture.id,
            "user_handle": "Test123",
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "user": updatedUser,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_user"]["profile_picture_updated_at"],
            str(updatedProfilePictureTime).replace(" ", "T"),
        )
