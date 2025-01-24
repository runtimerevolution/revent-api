import random

from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TransactionTestCase

from photo.models import Contest, ContestSubmission, Picture, User
from photo.tests.factories import ContestSubmissionFactory, PictureFactory, UserFactory


class ContestSubmissionTest(TransactionTestCase):
    def setUp(self):
        self.batch_size = random.randint(0, 3)
        self.votes = UserFactory.create_batch(
            self.batch_size, user_profile_picture=True
        )
        self.contest_submission = ContestSubmissionFactory(submission_votes=self.votes)

    def test_factory_create(self):
        self.assertEqual(ContestSubmission.objects.count(), 1)
        self.assertEqual(ContestSubmission.objects.first(), self.contest_submission)
        # 1 picture for the submission another for the contest cover picture
        self.assertEqual(Picture.objects.count(), 1 + 1)
        self.assertEqual(User.objects.count(), 2 + self.batch_size)

    def test_factory_null(self):
        with self.assertRaises(Contest.DoesNotExist):
            ContestSubmissionFactory(contest=None)
        with self.assertRaises(Picture.DoesNotExist):
            ContestSubmissionFactory(picture=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            ContestSubmissionFactory(id=self.contest_submission.id)

    def test_second_submission_same_user(self):
        with self.assertRaises(ValidationError):
            ContestSubmissionFactory(
                picture=PictureFactory(user=self.contest_submission.picture.user),
                contest=self.contest_submission.contest,
            )

    def test_created_at_and_updated_at_nullable(self):
        submission = ContestSubmission.objects.create(contest=self.contest_submission.contest, picture=self.contest_submission.picture)
        self.assertIsNotNone(submission.created_at)
        self.assertIsNone(submission.updated_at)

    def test_created_at_and_updated_at_update(self):
        submission = ContestSubmission.objects.create(contest=self.contest_submission.contest, picture=self.contest_submission.picture)
        submission.save()
        self.assertIsNotNone(submission.updated_at)
