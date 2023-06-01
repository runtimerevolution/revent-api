import pytest
from django.test import TestCase

from photo.schema import schema
from tests.factories import UserFactory
from tests.test_mutations.mutation_file import picture_creation_mutation
from tests.test_queries.query_file import user_query_one


class UserTest(TestCase):
    def setUp(self):
        newUser = UserFactory(user_profile_picture=True)

        newUserResult = schema.execute_sync(
            user_query_one,
            variable_values={"email": newUser.email},
        )
        self.newUser = newUserResult.data["users"][0]

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = picture_creation_mutation
        newUser = self.newUser
        newPicture = {
            "user": newUser,
            "picture_path": "www.test.com",
            "likes": {"email": newUser["email"]},
        }

        result = await schema.execute(
            mutation,
            variable_values={"picture": newPicture},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["create_picture"], newPicture)

    @pytest.mark.asyncio
    async def test_create_fail(self):
        newUser = self.newUser

        mutation = picture_creation_mutation
        newPicture = {
            "user": newUser,
            "picture_path": "www.test.com",
            "likes": {"email": newUser["email"]},
        }

        newPicture2 = {
            "user": newUser,
            "picture_path": "www.test.com",
            "likes": {"email": newUser["email"]},
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
