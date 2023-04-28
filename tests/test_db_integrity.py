from django.forms import ValidationError
from django.test import TestCase

from photo.models import Contest, ContestSubmission, Picture, PictureComment, User
from tests.factories import PictureCommentFactory, PictureFactory, UserFactory


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
        self.newPicture = PictureFactory()

    def test_factory(self):
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(Picture.objects.first(), self.newPicture)
        self.assertEqual(User.objects.count(), (1 + self.newPicture.likes.count()))
        self.assertEqual(User.objects.first(), self.newPicture.user)
        for like in self.newPicture.likes:
            self.assertTrue(User.objects.filter(email=like).exists())


class PictureCommentTest(TestCase):
    def setUp(self):
        self.newPictureComment = PictureCommentFactory()

    def test_factory(self):
        self.assertEqual(PictureComment.objects.count(), 1)
        self.assertEqual(PictureComment.objects.first(), self.newPictureComment)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(Picture.objects.first(), self.newPictureComment.picture)
        self.assertEqual(User.objects.count(), 2)
