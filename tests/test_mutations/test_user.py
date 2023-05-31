import pytest
from django.test import TestCase

from photo.schema import schema
from tests.test_mutations.mutation_file import user_creation_mutation


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
