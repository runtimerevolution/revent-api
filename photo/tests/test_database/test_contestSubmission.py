import random

from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TransactionTestCase

from photo.models import Contest, ContestSubmission, Picture, User
from photo.tests.factories import ContestSubmissionFactory, PictureFactory, UserFactory


class ContestSubmissionTest(TransactionTestCase):
    def setUp(self):
        self.batch = random.randint(0, 3)
        self.votes = UserFactory.create_batch(self.batch, user_profile_picture=True)
        self.newContestSubmission = ContestSubmissionFactory(
            submission_votes=self.votes
        )

    def test_factory_create(self):
        self.assertEqual(ContestSubmission.objects.count(), 1)
        self.assertEqual(ContestSubmission.objects.first(), self.newContestSubmission)
        # 1 picture for the submission another for the contest cover picture
        self.assertEqual(Picture.objects.count(), 1 + 1)
        self.assertEqual(User.objects.count(), 2 + self.batch)

    def test_factory_null(self):
        with self.assertRaises(Contest.DoesNotExist):
            ContestSubmissionFactory(contest=None)
        with self.assertRaises(Picture.DoesNotExist):
            ContestSubmissionFactory(picture=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            ContestSubmissionFactory(id=self.newContestSubmission.id)

    def test_second_submission_same_user(self):
        with self.assertRaises(ValidationError):
            ContestSubmissionFactory(
                picture=PictureFactory(user=self.newContestSubmission.picture.user),
                contest=self.newContestSubmission.contest,
            )
