import pytest
from django.test import TestCase
from tests.factories import PictureCommentFactory, PictureFactory, UserFactory
from tests.test_mutations.mutation_file import (
    picture_comment_creation_mutation,
    picture_comment_update_mutation,
)

from photo.schema import schema


class PictureCommentTest(TestCase):
    def setUp(self):
        self.newUser = UserFactory(user_profile_picture=True)
        self.newPicture = PictureFactory()

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = picture_comment_creation_mutation
        newUser = self.newUser
        newPicture = self.newPicture
        newPictureComment = {
            "user": newUser.email,
            "picture": newPicture.id,
            "text": "Random text",
        }

        result = await schema.execute(
            mutation,
            variable_values={"pictureComment": newPictureComment},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_pictureComment"]["user"]["email"], newUser.email
        )
        self.assertEqual(
            result.data["create_pictureComment"]["picture"]["id"],
            newPicture.id,
        )
        self.assertEqual(
            result.data["create_pictureComment"]["text"], newPictureComment["text"]
        )

    def test_update(self):
        mutation = picture_comment_update_mutation

        newPictureComment = PictureCommentFactory()
        updatedPictureComment = {
            "id": newPictureComment.id,
            "text": "test text",
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "pictureComment": updatedPictureComment,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_pictureComment"]["user"]["email"],
            newPictureComment.user.email,
        )
        self.assertEqual(
            result.data["update_pictureComment"]["picture"]["id"],
            newPictureComment.picture.id,
        )
        self.assertEqual(
            result.data["update_pictureComment"]["text"], updatedPictureComment["text"]
        )
