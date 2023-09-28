import pytest
from django.test import TestCase

from photo.schema import schema
from photo.tests.factories import PictureFactory, UserFactory
from .mutation_file import (
    picture_creation_mutation,
    picture_like_mutation,
    picture_update_mutation,
)
from strawberry.file_uploads import Upload


class PictureTest(TestCase):
    def setUp(self):
        self.newUser = UserFactory(user_profile_picture=True)
        self.newLikesUsers = UserFactory.create_batch(3, user_profile_picture=True)

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = picture_creation_mutation
        newUser = self.newUser
        newLikesUsers = self.newLikesUsers
        file_upload = Upload(
            b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00\x60\x00\x60\x00\x00...",
        )
        newPicture = {
            "user": str(newUser.id),
            "file": "www.test.com",
            "likes": [str(user.id) for user in newLikesUsers],
        }

        result = await schema.execute(
            mutation,
            variable_values={"picture": newPicture, "upload": file_upload},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_picture"]["user"]["email"], newPicture["user"]
        )
        self.assertEqual(result.data["create_picture"]["file"], newPicture["file"])
        self.assertEqual(
            len(result.data["create_picture"]["likes"]), len(newPicture["likes"])
        )

    @pytest.mark.asyncio
    async def test_create_fail(self):
        newUser = self.newUser

        mutation = picture_creation_mutation
        newPicture = {
            "user": str(newUser.id),
            "file": "www.test.com",
        }

        newPicture2 = {
            "user": str(newUser.id),
            "file": "www.test.com",
        }

        result = await schema.execute(
            mutation,
            variable_values={"picture": newPicture},
        )

        resultError = await schema.execute(
            mutation,
            variable_values={"picture": newPicture2},
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(resultError.errors, None)
        self.assertFalse(resultError.data["create_picture"]["__typename"] is None)
        self.assertEqual(
            resultError.data["create_picture"]["messages"][0]["message"],
            "Picture with this Picture path already exists.",
        )

    def test_like(self):
        mutation = picture_like_mutation

        newUser = UserFactory()
        newPicture = PictureFactory(user=newUser)
        newUserLike = UserFactory()

        result = schema.execute_sync(
            mutation,
            variable_values={
                "user": str(newUserLike.id),
                "picture": newPicture.id,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["like_picture"]["user"]["id"], str(newPicture.user.id)
        )
        self.assertEqual(
            result.data["like_picture"]["likes"][0]["id"], str(newUserLike.id)
        )

    def test_update(self):
        mutation = picture_update_mutation

        newUser = UserFactory()
        newPicture = PictureFactory(user=newUser, file="www.test.com")
        newUserLikes = UserFactory.create_batch(3)
        likes = [str(user.id) for user in newUserLikes]
        updatedPicture = {
            "id": newPicture.id,
            "likes": likes,
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "picture": updatedPicture,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["update_picture"]["user"]["id"], str(newUser.id))
        self.assertEqual(len(result.data["update_picture"]["likes"]), len(newUserLikes))
        for like in result.data["update_picture"]["likes"]:
            self.assertTrue(like["id"] in likes)
