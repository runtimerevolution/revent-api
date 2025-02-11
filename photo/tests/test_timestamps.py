from django.test import TestCase
from django.utils import timezone
from photo.models import User, Picture, Collection, Contest, ContestSubmission
from django.core.files.uploadedfile import SimpleUploadedFile


class TimestampFieldsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name_first="Test",
            name_last="User"
        )

        self.picture = Picture.objects.create(
            user=self.user,
            name="Test Picture",
            file=SimpleUploadedFile(
                "test.jpg",
                b"file_content",
                content_type="image/jpeg"
            )
        )

    def test_timestamp_fields_on_create(self):
        """Test that created_at and updated_at are set on model creation"""
        collection = Collection.objects.create(
            name="Test Collection",
            user=self.user
        )

        self.assertIsNotNone(collection.created_at)
        self.assertIsNotNone(collection.updated_at)
        self.assertIsInstance(collection.created_at, timezone.datetime)
        self.assertIsInstance(collection.updated_at, timezone.datetime)
        self.assertEqual(collection.created_at.date(), timezone.now().date())
        self.assertEqual(collection.updated_at.date(), timezone.now().date())

    def test_updated_at_changes_on_update(self):
        """Test that updated_at changes when model is updated"""
        collection = Collection.objects.create(
            name="Test Collection",
            user=self.user
        )
        original_updated_at = collection.updated_at

        # Wait a moment to ensure time difference
        import time
        time.sleep(0.1)

        collection.name = "Updated Collection"
        collection.save()

        self.assertNotEqual(collection.updated_at, original_updated_at)
        self.assertEqual(collection.created_at.date(), timezone.now().date())
        self.assertEqual(collection.updated_at.date(), timezone.now().date())
