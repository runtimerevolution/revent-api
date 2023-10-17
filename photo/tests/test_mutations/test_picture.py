from django.conf import settings
from django.test import TestCase
from PIL import Image

from integrations.aws.s3 import Client
from photo.models import Picture
from photo.schema import schema
from photo.tests.factories import UserFactory

from .graphql_mutations import picture_creation_mutation


class PictureTest(TestCase):
    def setUp(self):
        self.user = UserFactory(user_profile_picture=True)
        self.client = Client()

    def test_create(self):
        image = Image.new(mode="RGB", size=(200, 200))

        picture = {
            "user": str(self.user.id),
        }

        result = schema.execute_sync(
            picture_creation_mutation,
            variable_values={"picture": picture, "upload": image},
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["create_picture"]["user"]["id"], picture["user"])

        picture_object = Picture.objects.get(user__id=picture["user"])
        self.assertEqual(
            result.data["create_picture"]["file"],
            "media/{0}/{1}".format(picture["user"], picture_object.id),
        )

        s3_object = self.client.get_object(
            bucket=settings.AWS_STORAGE_BUCKET_NAME, key=picture_object.file.name
        )

        self.assertEqual(s3_object["ContentType"], "image/jpeg")
