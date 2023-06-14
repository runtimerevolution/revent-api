import pytest
from django.test import TestCase

from photo.schema import schema
from tests.factories import PictureFactory, UserFactory
from tests.test_mutations.mutation_file import (
    picture_creation_mutation,
    picture_like_mutation,
)
from tests.test_queries.query_file import user_query_one


class PictureTest(TestCase):
    def setUp(self):
        newUser = UserFactory(user_profile_picture=True)
        self.newLikesUsers = UserFactory.create_batch(3, user_profile_picture=True)

        newUserResult = schema.execute_sync(
            user_query_one,
            variable_values={"email": newUser.email},
        )
        self.newUser = newUserResult.data["users"][0]

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = picture_creation_mutation
        newUser = self.newUser
        newLikesUsers = self.newLikesUsers
        newPicture = {
            "user": newUser["email"],
            "picture_path": "www.test.com",
            "likes": [user.email for user in newLikesUsers],
        }

        result = await schema.execute(
            mutation,
            variable_values={"picture": newPicture},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_picture"]["user"]["email"], newPicture["user"]
        )
        self.assertEqual(
            result.data["create_picture"]["picture_path"], newPicture["picture_path"]
        )
        self.assertEqual(
            len(result.data["create_picture"]["likes"]), len(newPicture["likes"])
        )

    @pytest.mark.asyncio
    async def test_create_fail(self):
        newUser = self.newUser

        mutation = picture_creation_mutation
        newPicture = {
            "user": newUser["email"],
            "picture_path": "www.test.com",
        }

        newPicture2 = {
            "user": newUser["email"],
            "picture_path": "www.test.com",
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
        newPicture = PictureFactory(user=newUser, picture_path="www.test.com")
        newUserLike = UserFactory()

        result = schema.execute_sync(
            mutation,
            variable_values={
                "user": newUserLike.email,
                "picture": newPicture.picture_path,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["like_picture"]["user"]["email"], newPicture.user.email
        )
        self.assertEqual(
            result.data["like_picture"]["likes"][0]["email"], newUserLike.email
        )
