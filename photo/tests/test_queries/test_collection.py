from django.test import TestCase
from tests.factories import CollectionFactory, PictureFactory, UserFactory
from tests.test_queries.query_file import (
    collections_query_all,
    collections_query_name,
    collections_query_one,
    collections_query_user,
    collections_query_user_email,
)

from photo.models import Collection
from photo.schema import schema


class CollectionTest(TestCase):
    def setUp(self):
        self.batch = 10
        newUser = UserFactory(user_profile_picture=True)
        self.newPictures = PictureFactory.create_batch(self.batch, user=newUser)
        self.newColletions = CollectionFactory.create_batch(
            self.batch, collection_pictures=self.newPictures
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
        newUser = UserFactory(user_profile_picture=True)
        newPictures = PictureFactory.create_batch(3, user=newUser)
        newColletion = CollectionFactory.create(collection_pictures=newPictures)

        query = collections_query_one

        result = schema.execute_sync(
            query,
            variable_values={
                "id": newColletion.id,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], newColletion.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["email"], newColletion.user.email
        )
        self.assertEqual(
            len(result.data["collections"][0]["pictures"]), len(newPictures)
        )

    def test_query_user_email(self):
        newUser = UserFactory(user_profile_picture=True)
        newPictures = PictureFactory.create_batch(3, user=newUser)
        newColletion = CollectionFactory.create(collection_pictures=newPictures)

        query = collections_query_user_email

        result = schema.execute_sync(
            query,
            variable_values={
                "user_email": newColletion.user.email,
                "name": newColletion.name,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], newColletion.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["email"], newColletion.user.email
        )
        self.assertEqual(
            len(result.data["collections"][0]["pictures"]), len(newPictures)
        )

    def test_query_by_name(self):
        newUser = UserFactory(user_profile_picture=True)
        newPictures = PictureFactory.create_batch(3, user=newUser)
        newColletion = CollectionFactory.create(collection_pictures=newPictures)

        query = collections_query_name

        result = schema.execute_sync(
            query,
            variable_values={"name": newColletion.name},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], newColletion.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["email"], newColletion.user.email
        )
        self.assertEqual(
            len(result.data["collections"][0]["pictures"]), len(newPictures)
        )

    def test_query_by_user(self):
        newUser = UserFactory(user_profile_picture=True)
        newPictures = PictureFactory.create_batch(3, user=newUser)
        newColletion = CollectionFactory.create(collection_pictures=newPictures)
        otherCollections = CollectionFactory.create_batch(3, user=newColletion.user)

        query = collections_query_user

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newColletion.user.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1 + len(otherCollections))
        for collection in result.data["collections"]:
            self.assertEqual(collection["user"]["email"], newColletion.user.email)
