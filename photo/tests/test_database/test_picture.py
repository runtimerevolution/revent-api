import random
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, TransactionTestCase
from PIL import Image

from integrations.aws.s3 import Client
from photo.models import Picture, User
from photo.tests.factories import PictureFactory, UserFactory


class PictureTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.likes_batch = random.randint(0, 5)
        self.like_users = UserFactory.create_batch(self.likes_batch)
        self.picture = PictureFactory.create(user_likes=self.like_users, user=self.user)

    def test_factory(self):
        # One picture is created by the factory and another is created by the User subFactory
        self.assertEqual(Picture.objects.count(), (1 + User.objects.count()))
        self.assertEqual(
            Picture.objects.filter(file=self.picture.file).first(),
            self.picture,
        )
        self.assertEqual(User.objects.count(), (1 + self.picture.likes.all().count()))
        for like in self.picture.likes.all():
            self.assertTrue(User.objects.filter(email=like.email).exists())

    def test_created_at_and_updated_at_nullable(self):
        picture = Picture.objects.create(user=self.user)
        self.assertIsNone(picture.created_at)
        self.assertIsNone(picture.updated_at)

    def test_created_at_and_updated_at_update(self):
        picture = Picture.objects.create(user=self.user)
        picture.save()
        self.assertIsNotNone(picture.updated_at)

class PictureUploadTest(TestCase):
    def setUp(self):
        image = Image.new(mode="RGB", size=(200, 200))
        image_bytes = BytesIO()
        image.save(image_bytes, format="webp")
        image_bytes.seek(0)
        self.image_file = SimpleUploadedFile(
            "test_image", image_bytes.getvalue(), content_type="image/webp"
        )
        self.client = Client()

    def test_upload(self):
        user = UserFactory()
        picture = Picture.objects.create(user=user, file=self.image_file)

        self.assertEqual(picture.file.name, f"media/{user.id}/test_image.webp")

        s3_object = self.client.get_object(
            bucket=settings.AWS_STORAGE_BUCKET_NAME, key=picture.file.name
        )

        self.assertEqual(s3_object["ContentType"], "image/webp")
