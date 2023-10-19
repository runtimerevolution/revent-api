import pytest
from django.test import TestCase

from photo.schema import schema
from photo.tests.factories import PictureCommentFactory, PictureFactory, UserFactory

from .graphql_mutations import (
    picture_comment_creation_mutation,
    picture_comment_update_mutation,
)


class PictureCommentTest(TestCase):
    def setUp(self):
        self.user = UserFactory(user_profile_picture=True)
        self.picture = PictureFactory()

    @pytest.mark.asyncio
    async def test_create(self):
        picture_comment = {
            "user": str(self.user.id),
            "picture": self.picture.id,
            "text": "Random text",
        }

        result = await schema.execute(
            picture_comment_creation_mutation,
            variable_values={"pictureComment": picture_comment},
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_picture_comment"]["user"]["id"], str(self.user.id)
        )
        self.assertEqual(
            result.data["create_picture_comment"]["picture"]["id"],
            self.picture.id,
        )
        self.assertEqual(
            result.data["create_picture_comment"]["text"], picture_comment["text"]
        )

    def test_update(self):
        picture_comment = PictureCommentFactory()
        updated_picture_comment = {
            "id": picture_comment.id,
            "text": "test text",
        }

        result = schema.execute_sync(
            picture_comment_update_mutation,
            variable_values={
                "pictureComment": updated_picture_comment,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_picture_comment"]["user"]["id"],
            str(picture_comment.user.id),
        )
        self.assertEqual(
            result.data["update_picture_comment"]["picture"]["id"],
            picture_comment.picture.id,
        )
        self.assertEqual(
            result.data["update_picture_comment"]["text"],
            updated_picture_comment["text"],
        )
