import random

from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TransactionTestCase
from tests.factories import ContestFactory, UserFactory

from photo.models import Contest, Picture, User


class ContestTest(TransactionTestCase):
    def setUp(self):
        self.batch = random.randint(0, 3)
        self.winners = UserFactory.create_batch(self.batch, user_profile_picture=True)
        self.newContest = ContestFactory.create(contest_winners=self.winners)

    def test_factory(self):
        self.assertEqual(Contest.objects.count(), 1)
        self.assertEqual(Contest.objects.first(), self.newContest)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1 + self.batch)
        for winner in self.newContest.winners.all():
            self.assertTrue(User.objects.filter(email=winner.email).exists())

    def test_factory_null(self):
        with self.assertRaises(ValidationError):
            ContestFactory(created_by=None)
        with self.assertRaises(IntegrityError):
            ContestFactory(title=None)
        with self.assertRaises(IntegrityError):
            ContestFactory(prize=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            ContestFactory(id=self.newContest.id)
