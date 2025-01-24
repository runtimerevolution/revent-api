import random

from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TransactionTestCase

from photo.models import Contest, Picture, User
from photo.tests.factories import ContestFactory, UserFactory


class ContestTest(TransactionTestCase):
    def setUp(self):
        self.batch_size = random.randint(0, 3)
        self.winners = UserFactory.create_batch(
            self.batch_size, user_profile_picture=True
        )
        self.contest = ContestFactory.create(contest_winners=self.winners)

    def test_factory(self):
        self.assertEqual(Contest.objects.count(), 1)
        self.assertEqual(Contest.objects.first(), self.contest)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1 + self.batch_size)
        for winner in self.contest.winners.all():
            self.assertTrue(User.objects.filter(email=winner.email).exists())

    def test_factory_null(self):
        with self.assertRaises(ValidationError):
            ContestFactory(created_by=None)
        with self.assertRaises(IntegrityError):
            ContestFactory(title=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            ContestFactory(id=self.contest.id)

    def test_created_at_and_updated_at_nullable(self):
        contest = Contest.objects.create(created_by=self.winners[0])
        self.assertIsNotNone(contest.created_at)
        self.assertIsNone(contest.updated_at)

    def test_created_at_and_updated_at_update(self):
        contest = Contest.objects.create(created_by=self.winners[0])
        contest.title = "New Title"
        contest.save()
        self.assertIsNotNone(contest.updated_at)
