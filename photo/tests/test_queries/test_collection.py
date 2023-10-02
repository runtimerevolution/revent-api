from django.test import TestCase

from photo.models import Collection
from photo.schema import schema
from photo.tests.factories import CollectionFactory, PictureFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    collections_query_all,
    collections_query_name,
    collections_query_one,
    collections_query_user,
    collections_query_user_name,
)


class CollectionTest(TestCase):
    def setUp(self):
        self.batch = 10
        user = UserFactory(user_profile_picture=True)
        self.pictures = PictureFactory.create_batch(self.batch, user=user)
        self.collections = CollectionFactory.create_batch(
            self.batch, collection_pictures=self.pictures
        )

    def test_query_all(self):
        query = collections_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), self.batch)
        self.assertEqual(len(result.data["collections"][0]["pictures"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["collections"][0].keys()]),
            sorted(
                [
                    field.name
                    for field in (
                        Collection._meta.fields + Collection._meta.many_to_many
                    )
                ]
            ),
        )

    def test_query_one(self):
        user = UserFactory(user_profile_picture=True)
        pictures = PictureFactory.create_batch(3, user=user)
        collection = CollectionFactory.create(collection_pictures=pictures)

        query = collections_query_one

        result = schema.execute_sync(
            query,
            variable_values={
                "id": collection.id,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], collection.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["id"], str(collection.user.id)
        )
        self.assertEqual(len(result.data["collections"][0]["pictures"]), len(pictures))

    def test_query_user_name(self):
        user = UserFactory(user_profile_picture=True)
        pictures = PictureFactory.create_batch(3, user=user)
        collection = CollectionFactory.create(collection_pictures=pictures)

        query = collections_query_user_name

        result = schema.execute_sync(
            query,
            variable_values={
                "user": str(collection.user.id),
                "name": collection.name,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], collection.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["id"], str(collection.user.id)
        )
        self.assertEqual(len(result.data["collections"][0]["pictures"]), len(pictures))

    def test_query_by_name(self):
        user = UserFactory(user_profile_picture=True)
        pictures = PictureFactory.create_batch(3, user=user)
        collection = CollectionFactory.create(collection_pictures=pictures)

        query = collections_query_name

        result = schema.execute_sync(
            query,
            variable_values={"name": str(collection.name)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], collection.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["id"], str(collection.user.id)
        )
        self.assertEqual(len(result.data["collections"][0]["pictures"]), len(pictures))

    def test_query_by_user(self):
        user = UserFactory(user_profile_picture=True)
        collections = CollectionFactory.create_batch(3, user=user)

        query = collections_query_user

        result = schema.execute_sync(
            query,
            variable_values={"user": str(user.id)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), len(collections))
        for collection in result.data["collections"]:
            self.assertEqual(collection["user"]["id"], str(user.id))
