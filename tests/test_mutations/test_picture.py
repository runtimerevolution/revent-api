import pytest
from django.test import TestCase

from photo.schema import schema
from tests.factories import UserFactory
from tests.test_mutations.mutation_file import picture_creation_mutation


class UserTest(TestCase):
    def setUp(self):
        self.newUser = UserFactory()

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = picture_creation_mutation
        newUser = self.newUser
        newPicture = {
            "user": newUser.__dict__,
            "picture_path": "www.test.com",
            "likes": {newUser.email},
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
        await schema.execute(
            picture_creation_mutation,
            variable_values={"email": self.newUser.email},
        )

        mutation = picture_creation_mutation
        newPicture = {
            "user": newUser.__dict__,
            "picture_path": "www.test.com",
            "likes": {newUser.email},
        }

        newPicture2 = {
            "user": newUser.__dict__,
            "picture_path": "www.test.com",
            "likes": {newUser.email},
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
