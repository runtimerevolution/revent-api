import pytest
from django.test import TestCase

from photo.schema import schema
from tests.factories import PictureFactory, UserFactory
from tests.test_mutations.mutation_file import picture_comment_creation_mutation
from tests.test_queries.query_file import picture_query_one, user_query_one


class PictureCommentTest(TestCase):
    def setUp(self):
        newUser = UserFactory(user_profile_picture=True)
        newPicture = PictureFactory()
        newUserResult = schema.execute_sync(
            user_query_one,
            variable_values={"email": newUser.email},
        )
        newPictureResult = schema.execute_sync(
            picture_query_one,
            variable_values={"picture_path": newPicture.picture_path},
        )
        self.newUser = newUserResult.data["users"][0]
        self.newPicture = newPictureResult.data["pictures"][0]

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = picture_comment_creation_mutation
        newUser = self.newUser
        newPicture = self.newPicture
        newPictureComment = {
            "user": newUser["email"],
            "picture": newPicture["picture_path"],
            "text": "Random text",
        }

        result = await schema.execute(
            mutation,
            variable_values={"pictureComment": newPictureComment},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_pictureComment"]["user"]["email"], newUser["email"]
        )
        self.assertEqual(
            result.data["create_pictureComment"]["picture"]["picture_path"],
            newPicture["picture_path"],
        )
        self.assertEqual(
            result.data["create_pictureComment"]["text"], newPictureComment["text"]
        )
