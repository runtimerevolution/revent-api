import pytest
from django.test import TestCase

from photo.models import User


class TestNamedUserManager(TestCase):
    def setUp(self):
        # Create users with different name combinations
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="password123",
            name_first="John",
            name_last="Doe"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="password123",
            name_first="",
            name_last="Smith"
        )
        self.user3 = User.objects.create_user(
            email="user3@example.com",
            password="password123",
            name_first="Jane",
            name_last=""
        )
        self.user4 = User.objects.create_user(
            email="user4@example.com",
            password="password123",
            name_first=None,
            name_last=None
        )

    def test_named_users_manager(self):
        # Get all named users
        named_users = User.named_users.all()

        # Should only include users with both first and last names
        self.assertEqual(named_users.count(), 1)
        self.assertIn(self.user1, named_users)
        self.assertNotIn(self.user2, named_users)
        self.assertNotIn(self.user3, named_users)
        self.assertNotIn(self.user4, named_users)

    def test_default_manager_unchanged(self):
        # Verify that the default manager still returns all users
        all_users = User.objects.all()
        self.assertEqual(all_users.count(), 4)
        self.assertIn(self.user1, all_users)
        self.assertIn(self.user2, all_users)
        self.assertIn(self.user3, all_users)
        self.assertIn(self.user4, all_users)
