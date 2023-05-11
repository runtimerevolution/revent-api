import random

from django.forms import ValidationError
from django.test import TestCase

from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from tests.factories import (
    CollectionFactory,
    ContestFactory,
    PictureCommentFactory,
    PictureFactory,
    UserFactory,
)


class DBIntegrityTest(TestCase):
    def test_unique_submission_per_contest(self):
        new_user = User.objects.create(email="email")
        picture_1 = Picture.objects.create(picture_path="picture_path_1", user=new_user)
        picture_2 = Picture.objects.create(picture_path="picture_path_2", user=new_user)

        new_contest = Contest.objects.create(description="description")

        contest_submission_1 = ContestSubmission.objects.create(
            contest=new_contest, picture=picture_1
        )

        with self.assertRaises(ValidationError):
            ContestSubmission.objects.create(contest=new_contest, picture=picture_2)

        self.assertEqual(ContestSubmission.objects.count(), 1)
        self.assertEqual(ContestSubmission.objects.first(), contest_submission_1)


class UserTest(TestCase):
    def setUp(self):
        self.newUser = UserFactory()

    def test_factory(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), self.newUser)
        self.assertEqual(Picture.objects.count(), 1)


class PictureTest(TestCase):
    def setUp(self):
        self.newUser = UserFactory()
        self.likesbatch = random.randint(0, 5)
        self.likeUsers = UserFactory.create_batch(self.batch, profile_picture=None)
        self.newPicture = PictureFactory(user_likes=self.likeUsers, user=self.newUser)

    def test_factory(self):
        # One picture is created by the factory and another is created by the User subFactory
        self.assertEqual(Picture.objects.count(), (1 + 1 + self.likesbatch))
        self.assertEqual(
            Picture.objects.filter(picture_path=self.newPicture.picture_path).first(),
            self.newPicture,
        )
        self.assertEqual(
            User.objects.count(), (1 + self.newPicture.likes.all().count())
        )
        for like in self.newPicture.likes.all():
            self.assertTrue(User.objects.filter(email=like.email).exists())


class PictureCommentTest(TestCase):
    def setUp(self):
        self.batch = random.randint(0, 5)
        self.newPictureComment = PictureCommentFactory(
            collection_pictures=(
                UserFactory.create_batch(self.batch, profile_picture=None)
            )
        )

    def test_factory_create(self):
        self.assertEqual(PictureComment.objects.count(), 1)
        self.assertEqual(PictureComment.objects.first(), self.newPictureComment)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(Picture.objects.first(), self.newPictureComment.picture)
        self.assertEqual(User.objects.count(), 2)

    def test_factory_null(self):
        self.assertRaises(
            Exception,
        )


class CollectionTest(TestCase):
    def setUp(self):
        self.batch = random.randint(0, 10)
        self.newUser = UserFactory(profile_picture=None)
        self.newPictures = PictureFactory.create_batch(self.batch, user=self.newUser)
        self.newCollection = CollectionFactory(
            collection_pictures=self.newPictures, user=self.newUser
        )

    def test_factory(self):
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(Collection.objects.first(), self.newCollection)
        self.assertEqual(Picture.objects.count(), self.batch)
        self.assertEqual(User.objects.count(), 1)


class ContestTest(TestCase):
    def setUp(self):
        self.batch = random.randint(0, 3)
        self.winners = UserFactory.create_batch(self.batch, profile_picture=None)
        self.newContest = ContestFactory(contest_winners=self.winners)

    def test_factory(self):
        self.assertEqual(Contest.objects.count(), 1)
        self.assertEqual(Contest.objects.first(), self.newContest)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1 + self.batch)
        for winner in self.newContest.winners.all():
            self.assertTrue(User.objects.filter(email=winner.email).exists())
