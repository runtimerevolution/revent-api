import pytest
from django.test import TestCase

from photo.schema import schema
from photo.tests.factories import CollectionFactory, PictureFactory, UserFactory
from .graphql_mutations import (
    collection_add_picture_mutation,
    collection_creation_mutation,
    collection_update_mutation,
)


class CollectionTest(TestCase):
    def setUp(self):
        self.user = UserFactory(user_profile_picture=True)
        self.pictures = PictureFactory.create_batch(10, user=self.user)

    @pytest.mark.asyncio
    async def test_create(self):
        collection = {
            "user": str(self.user.id),
            "name": "Best collection",
            "pictures": [picture.id for picture in self.pictures],
        }

        result = await schema.execute(
            collection_creation_mutation,
            variable_values={"collection": collection},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_collection"]["user"]["id"], str(self.user.id)
        )
        self.assertEqual(
            len(result.data["create_collection"]["pictures"]), len(self.pictures)
        )
        for picture in result.data["create_collection"]["pictures"]:
            self.assertTrue(picture["id"] in collection["pictures"])
        self.assertEqual(result.data["create_collection"]["name"], collection["name"])

    @pytest.mark.asyncio
    async def test_create_fail(self):
        collection = {
            "user": str(self.user.id),
            "name": "Best collection",
            "pictures": [picture.id for picture in self.pictures],
        }

        result = await schema.execute(
            collection_creation_mutation,
            variable_values={"collection": collection},
        )

        result_error = await schema.execute(
            collection_creation_mutation,
            variable_values={"collection": collection},
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(result_error.errors, None)
        self.assertFalse(result_error.data["create_collection"]["__typename"] is None)
        self.assertEqual(
            result_error.data["create_collection"]["messages"][0],
            {
                "field": None,
                "kind": "VALIDATION",
                "message": "Collection with this Name and User already exists.",
            },
        )

    def test_add_picture(self):
        collection = CollectionFactory()
        picture = PictureFactory(file="www.test.com")

        result = schema.execute_sync(
            collection_add_picture_mutation,
            variable_values={
                "collection": collection.id,
                "picture": picture.id,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["collection_add_picture"]["pictures"][0]["id"],
            picture.id,
        )

    def test_update(self):
        user = UserFactory()
        old_pictures = PictureFactory.create_batch(5, user=user)
        collection = CollectionFactory(user=user, collection_pictures=old_pictures)
        new_pictures = PictureFactory.create_batch(10, user=user)

        pictures = [picture.id for picture in new_pictures]
        update_collection = {
            "id": collection.id,
            "name": "test name",
            "pictures": pictures,
        }

        result = schema.execute_sync(
            collection_update_mutation,
            variable_values={
                "collection": update_collection,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_collection"]["name"], update_collection["name"]
        )
        self.assertEqual(
            len(result.data["update_collection"]["pictures"]), len(new_pictures)
        )
        for picture in result.data["update_collection"]["pictures"]:
            self.assertTrue(picture["id"] in pictures)
