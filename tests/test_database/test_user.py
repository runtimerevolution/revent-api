from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Picture, User
from tests.factories import UserFactory


class UserTest(TransactionTestCase):
    def setUp(self):
        self.newUser = UserFactory()

    def test_factory(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), self.newUser)
        self.assertEqual(Picture.objects.count(), 1)

    def test_integity(self):
        self.assertEqual(
            User.objects.first().email, User.objects.first().profile_picture.user.email
        )
        self.assertEqual(
            Picture.objects.first().picture_path,
            User.objects.first().profile_picture.picture_path,
        )

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            UserFactory(email=self.newUser.email)
