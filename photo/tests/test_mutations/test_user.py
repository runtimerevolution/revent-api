from django.test import TestCase
from django.utils import timezone

from photo.models import User
from photo.schema import schema
from photo.tests.factories import PictureFactory, UserFactory

from .graphql_mutations import user_delete_mutation, user_update_mutation


class UserTest(TestCase):
    def test_update(self):
        update_profile_picture_time = timezone.datetime(2020, 4, 1, tzinfo=timezone.utc)
        user = UserFactory(profile_picture_updated_at=update_profile_picture_time)
        picture = PictureFactory(user=user)
        updatedUser = {
            "pk": str(user.id),
            "email": user.email,
            "name_first": "John",
            "name_last": "Smith",
            "profile_picture": picture.id,
            "user_handle": "johnSmithHandle",
        }

        result = schema.execute_sync(
            user_update_mutation,
            variable_values={
                "user": updatedUser,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["update_user"]["email"], user.email)
        self.assertEqual(
            result.data["update_user"]["name_first"], updatedUser["name_first"]
        )
        self.assertEqual(
            result.data["update_user"]["name_last"], updatedUser["name_last"]
        )
        self.assertEqual(
            result.data["update_user"]["profile_picture"]["id"],
            updatedUser["profile_picture"],
        )
        self.assertEqual(
            result.data["update_user"]["user_handle"], updatedUser["user_handle"]
        )
        self.assertFalse(
            result.data["update_user"]["profile_picture_updated_at"]
            == str(update_profile_picture_time).replace(" ", "T")
        )

    def test_update_profile_picture_updated_at(self):
        update_profile_picture_time = timezone.datetime(2020, 4, 1, tzinfo=timezone.utc)
        user = UserFactory(profile_picture_updated_at=update_profile_picture_time)
        updated_user = {
            "pk": str(user.id),
            "email": user.email,
            "name_first": "Test1",
            "name_last": "Test2",
            "profile_picture": user.profile_picture.id,
            "user_handle": "Test123",
        }

        result = schema.execute_sync(
            user_update_mutation,
            variable_values={
                "user": updated_user,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_user"]["profile_picture_updated_at"],
            str(update_profile_picture_time).replace(" ", "T"),
        )

    def test_delete_success(self):
        user = UserFactory()

        result = schema.execute_sync(
            user_delete_mutation,
            variable_values={
                "user": {"id": str(user.id)},
            },
        )

        queryset_undeleted = User.objects.filter(id=user.id)
        queryset_all = User.all_objects.filter(id=user.id)

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["delete_user"]["id"], str(user.id))
        self.assertEqual(queryset_undeleted.count(), 1)
        self.assertEqual(queryset_all.count(), 1)
        self.assertEqual(queryset_all[0].id, user.id)
