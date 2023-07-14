import random

from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Picture, User
from tests.factories import PictureFactory, UserFactory


class PictureTest(TransactionTestCase):
    def setUp(self):
        self.newUser = UserFactory.create()
        self.likesbatch = random.randint(0, 5)
        self.likeUsers = UserFactory.create_batch(self.likesbatch)
        self.newPicture = PictureFactory.create(
            user_likes=self.likeUsers, user=self.newUser
        )

    def test_factory(self):
        # One picture is created by the factory and another is created by the User subFactory
        self.assertEqual(Picture.objects.count(), (1 + User.objects.count()))
        self.assertEqual(
            Picture.objects.filter(picture_path=self.newPicture.picture_path).first(),
            self.newPicture,
        )
        self.assertEqual(
            User.objects.count(), (1 + self.newPicture.likes.all().count())
        )
        for like in self.newPicture.likes.all():
            self.assertTrue(User.objects.filter(email=like.email).exists())

    def test_factory_null(self):
        with self.assertRaises(IntegrityError):
            PictureFactory(user=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            PictureFactory(id=self.newPicture.id)
        with self.assertRaises(IntegrityError):
            PictureFactory(picture_path=self.newPicture.picture_path)
