from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Picture, PictureComment, User
from tests.factories import PictureCommentFactory


class PictureCommentTest(TransactionTestCase):
    def setUp(self):
        self.newPictureComment = PictureCommentFactory.create()

    def test_factory_create(self):
        self.assertEqual(PictureComment.objects.count(), 1)
        self.assertEqual(PictureComment.objects.first(), self.newPictureComment)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(Picture.objects.first(), self.newPictureComment.picture)
        self.assertEqual(User.objects.count(), 2)

    def test_factory_null(self):
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(user=None)
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(picture=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(id=self.newPictureComment.id)
