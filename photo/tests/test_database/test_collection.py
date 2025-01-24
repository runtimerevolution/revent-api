import random

from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Collection, Picture, User
from photo.tests.factories import CollectionFactory, PictureFactory, UserFactory


class CollectionTest(TransactionTestCase):
    def setUp(self):
        self.batch_size = random.randint(0, 10)
        self.user = UserFactory.create(user_profile_picture=True)
        self.pictures = PictureFactory.create_batch(self.batch_size, user=self.user)
        self.collection = CollectionFactory(
            collection_pictures=self.pictures, user=self.user
        )

    def test_factory(self):
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(Collection.objects.first(), self.collection)
        self.assertEqual(Picture.objects.count(), self.batch_size)
        self.assertEqual(User.objects.count(), 1)

    def test_factory_null(self):
        with self.assertRaises(IntegrityError):
            CollectionFactory(user=None)
        with self.assertRaises(IntegrityError):
            CollectionFactory(name=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            CollectionFactory(user=self.collection.user, name=self.collection.name)

    def test_created_at_and_updated_at_nullable(self):
        collection = Collection.objects.create(user=self.user)
        self.assertIsNotNone(collection.created_at)
        self.assertIsNotNone(collection.updated_at)

    def test_created_at_and_updated_at_update(self):
        collection = Collection.objects.create(user=self.user)
        collection.name = "New Name"
        collection.save()
        self.assertIsNotNone(collection.updated_at)
