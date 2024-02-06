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
            variable_values={
                "user": str(user_like.id),
                "picture": picture.id,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["like_picture"]["results"]["user"]["id"], str(picture.user.id)
        )
        self.assertEqual(
            result.data["like_picture"]["results"]["likes"][0]["id"], str(user_like.id)
        )

    def test_update(self):
        user = UserFactory()
        picture = PictureFactory(user=user)
        user_like = UserFactory.create_batch(3)
        likes = [str(user.id) for user in user_like]
        updatedPicture = {
            "id": picture.id,
            "likes": likes,
        }

        result = schema.execute_sync(
            picture_update_mutation,
            variable_values={
                "picture": updatedPicture,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["update_picture"]["user"]["id"], str(user.id))
        self.assertEqual(len(result.data["update_picture"]["likes"]), len(user_like))
        for like in result.data["update_picture"]["likes"]:
            self.assertTrue(like["id"] in likes)

    def test_delete_success(self):
        picture = PictureFactory()

        result = schema.execute_sync(
            picture_delete_mutation,
            variable_values={
                "picture": {"id": picture.id},
            },
        )

        queryset_undeleted = Picture.objects.filter(id=picture.id)
        queryset_all = Picture.all_objects.filter(id=picture.id)

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["delete_picture"]["id"], picture.id)
        self.assertEqual(queryset_undeleted.count(), 0)
        self.assertEqual(queryset_all.count(), 1)
        self.assertEqual(queryset_all[0].id, picture.id)
