
from django.conf import settings
from django.test import TestCase
from PIL import Image

from integrations.aws.s3 import Client
from photo.models import Picture
from photo.schema import schema
from photo.tests.factories import PictureFactory, UserFactory

from .graphql_mutations import (
    picture_creation_mutation,
    picture_delete_mutation,
    picture_like_mutation,
    picture_update_mutation,
)

class PictureTest(TestCase):
    def setUp(self):
        self.user = UserFactory(user_profile_picture=True)
        self.client = Client()
        self.liked_users = UserFactory.create_batch(3, user_profile_picture=True)

    def test_create(self):
        image = Image.new(mode="RGB", size=(200, 200))

        picture = {
            "user": str(self.user.id),
            "file": image,
            "description": "Test Description"
        }

        result = schema.execute_sync(
            picture_creation_mutation,
            variable_values={"input": picture},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_picture"]["results"]["user"]["id"], picture["user"]
        )

        picture_object = Picture.objects.get(user__id=picture["user"])
        self.assertEqual(
            result.data["create_picture"]["results"]["file"],
            "media/{0}/{1}.webp".format(picture["user"], picture_object.id),
        )
          
        self.assertEqual(
            result.data["create_picture"]["results"]["description"],
            picture["description"],
        )

        s3_object = self.client.get_object(
            bucket=settings.AWS_STORAGE_BUCKET_NAME, key=picture_object.file.name
        )

        self.assertEqual(s3_object["ContentType"], "image/webp")

    def test_like(self):
        user = UserFactory()
        picture = PictureFactory(user=user)
        user_like = UserFactory()

        result = schema.execute_sync(
            picture_like_mutation,
            variable_values={"pictureId": picture.id},
        )

        self.assertEqual(result.errors, None)
        picture.refresh_from_db()
        self.assertTrue(user in picture.likes.all())

class PictureTest(TestCase):
    def setUp(self):
        self.user = UserFactory(user_profile_picture=True)
        self.client = Client()
        self.liked_users = UserFactory.create_batch(3, user_profile_picture=True)

    def test_create(self):
        image = Image.new(mode="RGB", size=(200, 200))

        picture = {
            "user": str(self.user.id),
            "file": image,
            "description": "Test Description"
        }