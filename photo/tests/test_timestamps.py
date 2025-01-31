from django.test import TestCase
from django.utils import timezone
from photo.models import User, Picture, Collection, Contest, ContestSubmission, PictureComment


class TimestampedModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )

    def test_timestamps_on_create(self):
        """Test that created_at and updated_at are set on model creation"""
        picture = Picture.objects.create(
            user=self.user,
            name="Test Picture"
        )

        self.assertIsNotNone(picture.created_at)
        self.assertIsNotNone(picture.updated_at)
        self.assertEqual(picture.created_at, picture.updated_at)

    def test_updated_at_changes_on_update(self):
        """Test that updated_at changes when model is updated"""
        collection = Collection.objects.create(
            name="Test Collection",
            user=self.user
        )
        initial_updated_at = collection.updated_at

        # Wait a moment to ensure timestamps will be different
        import time
        time.sleep(0.1)

        collection.name = "Updated Collection"
        collection.save()

        self.assertEqual(collection.created_at, initial_updated_at)
        self.assertGreater(collection.updated_at, initial_updated_at)

    def test_timestamps_nullable(self):
        """Test that timestamp fields are nullable"""
        # Force created_at and updated_at to be None
        contest = Contest.objects.create(
            title="Test Contest",
            description="Test Description",
            created_by=self.user,
            created_at=None,
            updated_at=None
        )

        self.assertIsNone(contest.created_at)
        self.assertIsNone(contest.updated_at)
