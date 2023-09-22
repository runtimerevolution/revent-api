import pytest
from django.test import TestCase
from tests.factories import CollectionFactory, PictureFactory, UserFactory
from tests.test_mutations.mutation_file import (
    collection_add_picture_mutation,
    collection_creation_mutation,
    collection_update_mutation,
)

from photo.schema import schema


class CollectionTest(TestCase):
    def setUp(self):
        self.newUser = UserFactory(user_profile_picture=True)
        self.newPictures = PictureFactory.create_batch(10, user=self.newUser)

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = collection_creation_mutation
        newUser = self.newUser

        newCollection = {
            "user": newUser.email,
            "name": "Best collection",
            "pictures": [picture.id for picture in self.newPictures],
        }

        result = await schema.execute(
            mutation,
            variable_values={"collection": newCollection},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_collection"]["user"]["email"], newUser.email
        )
        self.assertEqual(
            len(result.data["create_collection"]["pictures"]), len(self.newPictures)
        )
        for picture in result.data["create_collection"]["pictures"]:
            self.assertTrue(picture["id"] in newCollection["pictures"])
        self.assertEqual(
            result.data["create_collection"]["name"], newCollection["name"]
        )

    @pytest.mark.asyncio
    async def test_create_fail(self):
        mutation = collection_creation_mutation
        newUser = self.newUser

        newCollection = {
            "user": newUser.email,
            "name": "Best collection",
            "pictures": [picture.id for picture in self.newPictures],
        }

        newCollection2 = {
            "user": newUser.email,
            "name": "Best collection",
            "pictures": [picture.id for picture in self.newPictures],
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

    def test_add_picture(self):
        mutation = collection_add_picture_mutation

        newCollection = CollectionFactory()
        newPicture = PictureFactory(picture_path="www.test.com")

        result = schema.execute_sync(
            mutation,
            variable_values={
                "collection": newCollection.id,
                "picture": newPicture.id,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["collection_add_picture"]["pictures"][0]["id"],
            newPicture.id,
        )

    def test_update(self):
        mutation = collection_update_mutation

        newUser = UserFactory()
        oldPictures = PictureFactory.create_batch(5, user=newUser)
        newCollection = CollectionFactory(user=newUser, collection_pictures=oldPictures)
        newPictures = PictureFactory.create_batch(10, user=newUser)

        pictures = [picture.id for picture in newPictures]
        updatedCollection = {
            "id": newCollection.id,
            "name": "test name",
            "pictures": pictures,
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "collection": updatedCollection,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_collection"]["name"], updatedCollection["name"]
        )
        self.assertEqual(
            len(result.data["update_collection"]["pictures"]), len(newPictures)
        )
        for picture in result.data["update_collection"]["pictures"]:
            self.assertTrue(picture["id"] in pictures)
