import pytest
from django.test import TestCase

from photo.schema import schema
from tests.factories import PictureFactory, UserFactory
from tests.test_mutations.mutation_file import collection_creation_mutation
from tests.test_queries.query_file import user_query_one


class PictureCommentTest(TestCase):
    def setUp(self):
        newUser = UserFactory(user_profile_picture=True)
        self.newPictures = PictureFactory.create_batch(10, user=newUser)

        newUserResult = schema.execute_sync(
            user_query_one,
            variable_values={"email": newUser.email},
        )
        self.newUser = newUserResult.data["users"][0]

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = collection_creation_mutation
        newUser = self.newUser

        newCollection = {
            "user": newUser["email"],
            "name": "Best collection",
            "pictures": [picture.picture_path for picture in self.newPictures],
        }

        result = await schema.execute(
            mutation,
            variable_values={"collection": newCollection},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_collection"]["user"]["email"], newUser["email"]
        )
        self.assertEqual(
            len(result.data["create_collection"]["pictures"]), len(self.newPictures)
        )
        for picture in result.data["create_collection"]["pictures"]:
            self.assertTrue(picture["picture_path"] in newCollection["pictures"])
        self.assertEqual(
            result.data["create_collection"]["name"], newCollection["name"]
        )

    @pytest.mark.asyncio
    async def test_create_fail(self):
        mutation = collection_creation_mutation
        newUser = self.newUser

        newCollection = {
            "user": newUser["email"],
            "name": "Best collection",
            "pictures": [picture.picture_path for picture in self.newPictures],
        }

        newCollection2 = {
            "user": newUser["email"],
            "name": "Best collection",
            "pictures": [picture.picture_path for picture in self.newPictures],
        }

        result = await schema.execute(
            mutation,
            variable_values={"collection": newCollection},
        )

        resultError = await schema.execute(
            mutation,
            variable_values={"collection": newCollection2},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(resultError.errors, None)
        self.assertFalse(resultError.data["create_collection"]["__typename"] is None)
        self.assertEqual(
            resultError.data["create_collection"]["messages"][0],
            {
                "field": None,
                "kind": "VALIDATION",
                "message": "Collection with this Name and User already exists.",
            },
        )
