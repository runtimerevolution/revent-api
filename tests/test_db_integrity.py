from django.forms import ValidationError
from django.test import TestCase

from photo.models import Contest, ContestSubmission, Picture, User


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
