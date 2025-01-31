from django.test import TestCase

from photo.models import Collection
from photo.schema import schema
from photo.tests.factories import CollectionFactory, PictureFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    collections_query_all,
    collections_query_filter,
)


class CollectionTest(TestCase):
    def setUp(self):
        self.batch_size = 10
        user = UserFactory(user_profile_picture=True)
        self.pictures = PictureFactory.create_batch(self.batch_size, user=user)
        self.collections = CollectionFactory.create_batch(
            self.batch_size, collection_pictures=self.pictures
        )

    def test_query_success(self):
        result = schema.execute_sync(
            collections_query_all,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), self.batch_size)
        self.assertEqual(
            len(result.data["collections"][0]["pictures"]), self.batch_size
        )
        self.assertEqual(
            sorted(
                [key for key in result.data["collections"][0].keys()]
            ),
            sorted(
                [
                    field.name
                    for field in (
                        Collection._meta.fields + Collection._meta.many_to_many
                    )
                    if field.name != "is_deleted"
                ]
            ),
        )

    def test_filter_by_id(self):
        user = UserFactory(user_profile_picture=True)
        pictures = PictureFactory.create_batch(3, user=user)
        collection = CollectionFactory.create(collection_pictures=pictures)

        result = schema.execute_sync(
            collections_query_filter,
            variable_values={
                "filters": {"id": collection.id},
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], collection.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["id"], str(collection.user.id)
        )
        self.assertEqual(len(result.data["collections"][0]["pictures"]), len(pictures))

    def test_filter_by_user_name(self):
        user = UserFactory(user_profile_picture=True)
        pictures = PictureFactory.create_batch(3, user=user)
        collection = CollectionFactory.create(collection_pictures=pictures)

        result = schema.execute_sync(
            collections_query_filter,
            variable_values={
                "filters": {
                    "user": {"id": str(collection.user.id)},
                    "name": collection.name,
                }
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], collection.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["id"], str(collection.user.id)
        )
        self.assertEqual(len(result.data["collections"][0]["pictures"]), len(pictures))

    def test_filter_by_name(self):
        user = UserFactory(user_profile_picture=True)
        pictures = PictureFactory.create_batch(3, user=user)
        collection = CollectionFactory.create(collection_pictures=pictures)

        result = schema.execute_sync(
            collections_query_filter,
            variable_values={"filters": {"name": str(collection.name)}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], collection.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["id"], str(collection.user.id)
        )
        self.assertEqual(len(result.data["collections"][0]["pictures"]), len(pictures))

    def test_filter_by_user(self):
        user = UserFactory(user_profile_picture=True)
        collections = CollectionFactory.create_batch(3, user=user)

        result = schema.execute_sync(
            collections_query_filter,
            variable_values={"filters": {"user": {"id": str(user.id)}}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), len(collections))
        for collection in result.data["collections"]:
            self.assertEqual(collection["user"]["id"], str(user.id))


class CollectionWithoutData(TestCase):
    def test_query_without_data(self):
        result = schema.execute_sync(
            collections_query_all,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 0)
