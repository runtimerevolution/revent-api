from django.test import TransactionTestCase
from django.utils import timezone
from datetime import timedelta

from photo.models import Collection, Contest, ContestSubmission, Picture, PictureComment, User
from photo.tests.factories import (
    CollectionFactory,
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    PictureCommentFactory,
    UserFactory,
)


class TimestampFieldsTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.picture = PictureFactory(user=self.user)
        self.collection = CollectionFactory(user=self.user)
        self.contest = ContestFactory(created_by=self.user)
        self.submission = ContestSubmissionFactory(
            contest=self.contest,
            picture=self.picture
        )
        self.comment = PictureCommentFactory(
            user=self.user,
            picture=self.picture
        )

    def test_created_at_on_creation(self):
        """Test that created_at is set on object creation"""
        now = timezone.now()

        # Test for each model
        self.assertIsNotNone(self.user.created_at)
        self.assertLess(self.user.created_at, now)

        self.assertIsNotNone(self.picture.created_at)
        self.assertLess(self.picture.created_at, now)

        self.assertIsNotNone(self.collection.created_at)
        self.assertLess(self.collection.created_at, now)

        self.assertIsNotNone(self.contest.created_at)
        self.assertLess(self.contest.created_at, now)

        self.assertIsNotNone(self.submission.created_at)
        self.assertLess(self.submission.created_at, now)

        self.assertIsNotNone(self.comment.created_at)
        self.assertLess(self.comment.created_at, now)

    def test_updated_at_on_creation(self):
        """Test that updated_at is set on object creation"""
        now = timezone.now()

        # Test for each model
        self.assertIsNotNone(self.user.updated_at)
        self.assertLess(self.user.updated_at, now)

        self.assertIsNotNone(self.picture.updated_at)
        self.assertLess(self.picture.updated_at, now)

        self.assertIsNotNone(self.collection.updated_at)
        self.assertLess(self.collection.updated_at, now)

        self.assertIsNotNone(self.contest.updated_at)
        self.assertLess(self.contest.updated_at, now)

        self.assertIsNotNone(self.submission.updated_at)
        self.assertLess(self.submission.updated_at, now)

        self.assertIsNotNone(self.comment.updated_at)
        self.assertLess(self.comment.updated_at, now)

    def test_updated_at_on_update(self):
        """Test that updated_at is updated when object is modified"""
        # Store initial timestamps
        user_updated = self.user.updated_at
        picture_updated = self.picture.updated_at
        collection_updated = self.collection.updated_at
        contest_updated = self.contest.updated_at
        submission_updated = self.submission.updated_at
        comment_updated = self.comment.updated_at

        # Wait a bit to ensure timestamps will be different
        timezone.sleep(timedelta(milliseconds=10))

        # Update each object
        self.user.name_first = "Updated"
        self.user.save()

        self.picture.name = "Updated Picture"
        self.picture.save()

        self.collection.name = "Updated Collection"
        self.collection.save()

        self.contest.title = "Updated Contest"
        self.contest.save()

        self.submission.submission_date = timezone.now()
        self.submission.save()

        self.comment.text = "Updated Comment"
        self.comment.save()

        # Verify updated_at was changed
        self.assertGreater(self.user.updated_at, user_updated)
        self.assertGreater(self.picture.updated_at, picture_updated)
        self.assertGreater(self.collection.updated_at, collection_updated)
        self.assertGreater(self.contest.updated_at, contest_updated)
        self.assertGreater(self.submission.updated_at, submission_updated)
        self.assertGreater(self.comment.updated_at, comment_updated)

    def test_created_at_unchanged_on_update(self):
        """Test that created_at remains unchanged when object is modified"""
        # Store initial timestamps
        user_created = self.user.created_at
        picture_created = self.picture.created_at
        collection_created = self.collection.created_at
        contest_created = self.contest.created_at
        submission_created = self.submission.created_at
        comment_created = self.comment.created_at

        # Update each object
        self.user.name_first = "Updated"
        self.user.save()

        self.picture.name = "Updated Picture"
        self.picture.save()

        self.collection.name = "Updated Collection"
        self.collection.save()

        self.contest.title = "Updated Contest"
        self.contest.save()

        self.submission.submission_date = timezone.now()
        self.submission.save()

        self.comment.text = "Updated Comment"
        self.comment.save()

        # Verify created_at was not changed
        self.assertEqual(self.user.created_at, user_created)
        self.assertEqual(self.picture.created_at, picture_created)
        self.assertEqual(self.collection.created_at, collection_created)
        self.assertEqual(self.contest.created_at, contest_created)
        self.assertEqual(self.submission.created_at, submission_created)
        self.assertEqual(self.comment.created_at, comment_created)
