import random

from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Collection, Picture, User
from tests.factories import CollectionFactory, PictureFactory, UserFactory


class CollectionTest(TransactionTestCase):
    def setUp(self):
        self.batch = random.randint(0, 10)
        self.newUser = UserFactory.create(user_profile_picture=True)
        self.newPictures = PictureFactory.create_batch(self.batch, user=self.newUser)
        self.newCollection = CollectionFactory(
            collection_pictures=self.newPictures, user=self.newUser
        )

    def test_factory(self):
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(Collection.objects.first(), self.newCollection)
        self.assertEqual(Picture.objects.count(), self.batch)
        self.assertEqual(User.objects.count(), 1)

    def test_factory_null(self):
        with self.assertRaises(IntegrityError):
            CollectionFactory(user=None)
        with self.assertRaises(IntegrityError):
            CollectionFactory(name=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            CollectionFactory(
                user=self.newCollection.user, name=self.newCollection.name
            )