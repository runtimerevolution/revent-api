from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Picture, PictureComment, User
from photo.tests.factories import PictureCommentFactory


class PictureCommentTest(TransactionTestCase):
    def setUp(self):
        self.picture_comment = PictureCommentFactory.create()

    def test_factory_create(self):
        self.assertEqual(PictureComment.objects.count(), 1)
        self.assertEqual(PictureComment.objects.first(), self.picture_comment)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(Picture.objects.first(), self.picture_comment.picture)
        self.assertEqual(User.objects.count(), 2)

    def test_factory_null(self):
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(user=None)
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(picture=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(id=self.picture_comment.id)

    def test_created_at_and_updated_at_nullable(self):
        comment = PictureComment.objects.create(user=self.picture_comment.user, picture=self.picture_comment.picture)
        self.assertIsNone(comment.created_at)
        self.assertIsNone(comment.updated_at)

    def test_created_at_and_updated_at_update(self):
        comment = PictureComment.objects.create(user=self.picture_comment.user, picture=self.picture_comment.picture)
        comment.save()
        self.assertIsNotNone(comment.updated_at)
