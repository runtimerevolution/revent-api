import factory
import pytz
from django.forms import ValidationError
from django.test import TestCase
from PIL import Image

from photo.fixtures import OUTDATED_SUBMISSION_ERROR_MESSAGE
from photo.models import ContestSubmission
from photo.schema import schema
from photo.tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)

from .graphql_mutations import (
    contest_submission_creation_mutation,
    contest_submission_delete_mutation,
    contest_submission_update_mutation,
    contest_submission_vote_mutation,
)


class ContestSubmissionTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.contest = ContestFactory()

    def test_create(self):
        image = Image.new(mode="RGB", size=(200, 200))
        contest_submission = {
            "picture": {
                "user": str(self.user.id),
                "file": image,
            },
            "contest": int(self.contest.id),
        }

        result = schema.execute_sync(
            contest_submission_creation_mutation,
            variable_values={"contestSubmission": contest_submission},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_contest_submission"]["results"]["picture"]["user"][
                "email"
            ],
            self.user.email,
        )

        self.assertEqual(
            result.data["create_contest_submission"]["results"]["contest"]["id"],
            self.contest.id,
        )

    def test_vote(self):
        contest_submission = ContestSubmissionFactory()
        user_vote = UserFactory()
        result = schema.execute_sync(
            contest_submission_vote_mutation,
            variable_values={
                "contestSubmission": contest_submission.id,
                "user": str(user_vote.id),
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submission_add_vote"]["results"]["votes"][0]["email"],
            user_vote.email,
        )

    def test_update(self):
        contest = ContestFactory()

        user = UserFactory()
        original_picture = PictureFactory(user=user)
        newContestSubmission = ContestSubmissionFactory(
            contest=contest, picture=original_picture
        )

        self.assertEqual(newContestSubmission.picture.file, original_picture.file)

        newPicture = {
            "user": str(user.id),
            "file": Image.new(mode="RGB", size=(200, 200)),
        }

        updated_contest_submission = {
            "id": newContestSubmission.id,
            "picture": newPicture,
        }

        result = schema.execute_sync(
            contest_submission_update_mutation,
            variable_values={
                "contestSubmission": updated_contest_submission,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertFalse(
            result.data["update_contest_submission"]["results"]["picture"]["id"]
            == str(original_picture.id)
        )

    def test_repeat_vote(self):
        contest_submission = ContestSubmissionFactory()
        user_vote = UserFactory()

        result = schema.execute_sync(
            contest_submission_vote_mutation,
            variable_values={
                "contestSubmission": contest_submission.id,
                "user": str(user_vote.id),
            },
        )

        result_error = schema.execute_sync(
            contest_submission_vote_mutation,
            variable_values={
                "contestSubmission": contest_submission.id,
                "user": str(user_vote.id),
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_submission_add_vote"]["results"]["votes"][0]["email"],
            user_vote.email,
        )
        self.assertEqual(result_error.errors, None)
        self.assertEqual(len(contest_submission.votes.all()), 1)

    def test_outdate_submission(self):
        contest = ContestFactory(
            upload_phase_end=factory.Faker("date_time", tzinfo=pytz.UTC)
        )
        with self.assertRaises(ValidationError) as e:
            ContestSubmissionFactory(contest=contest)

        exception = e.exception
        self.assertIn(OUTDATED_SUBMISSION_ERROR_MESSAGE, exception.messages)

    def test_delete_success(self):
        contest_submission = ContestSubmissionFactory()

        result = schema.execute_sync(
            contest_submission_delete_mutation,
            variable_values={
                "contest_submission": {"id": contest_submission.id},
            },
        )

        queryset_undeleted = ContestSubmission.objects.filter(id=contest_submission.id)
        queryset_all = ContestSubmission.all_objects.filter(id=contest_submission.id)

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["delete_contest_submission"]["id"], contest_submission.id
        )
        self.assertEqual(queryset_undeleted.count(), 0)
        self.assertEqual(queryset_all.count(), 1)
        self.assertEqual(queryset_all[0].id, contest_submission.id)
