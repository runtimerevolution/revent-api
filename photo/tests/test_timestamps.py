from django.test import TestCase
from django.utils import timezone

from photo.models import Collection, User


class TimestampFieldsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name_first="Test",
            name_last="User",
        )

    def test_timestamp_fields(self):
        # Create a collection and verify timestamps are set
        collection = Collection.objects.create(
            name="Test Collection",
            user=self.user,
        )
        self.assertIsNotNone(collection.created_at)
        self.assertIsNotNone(collection.updated_at)
        self.assertEqual(collection.created_at, collection.updated_at)

        # Store the original timestamps
        original_created_at = collection.created_at
        original_updated_at = collection.updated_at

        # Wait a moment to ensure timestamps will be different
        timezone.now()

        # Update the collection and verify only updated_at changes
        collection.name = "Updated Collection"
        collection.save()
        collection.refresh_from_db()

        self.assertEqual(collection.created_at, original_created_at)
        self.assertGreater(collection.updated_at, original_updated_at)
