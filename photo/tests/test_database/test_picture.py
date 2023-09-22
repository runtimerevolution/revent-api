import random
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from PIL import Image
from tests.factories import PictureFactory, UserFactory

from integrations.aws.s3 import Client
from photo.models import Picture, User


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


class PictureUploadTest(TestCase):
    def setUp(self):
        image = Image.new(mode="RGB", size=(200, 200))
        image_bytes = BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        self.image_file = SimpleUploadedFile(
            "test_image.jpg", image_bytes.getvalue(), content_type="image/jpeg"
        )

    def test_upload(self):
        picture = Picture.objects.create(
            user=UserFactory(), picture_path=self.image_file
        )

        self.assertEqual(picture.picture_path.name, "sample/test_image.jpg")

        s3_object = Client.get_object(
            bucket=settings.AWS_STORAGE_BUCKET_NAME, key="sample/test_image.jpg"
        )
        print(s3_object)
