import pytest
from django.test import TestCase
from PIL import Image


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

    def test_create_one(self):
        mutation = picture_creation_mutation
        newUser = self.newUser
        image = Image.new(mode="RGB", size=(200, 200))

        newPicture = {
            "user": str(newUser.id),
        }

        result = schema.execute_sync(
            mutation,
            variable_values={"picture": newPicture, "upload": image},
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_picture"]["user"]["id"], newPicture["user"]
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
