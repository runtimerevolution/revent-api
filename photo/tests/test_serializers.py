import pytest
import datetime
from photo import models
from photo.tests.factories import (
    UserFactory,
    ContestFactory,
    SubmissionFactory,
    CommentFactory,
    VoteFactory,
    ResultFactory,
)

from photo.serializers import (
    UserSerializer,
    ContestSerializer,
    SubmissionSerializer,
    CommentSerializer,
    VoteSerializer,
    ResultSerializer,
)


class TestSerializers:
    def setUp(self):
        UserFactory(first_name="TestSetUp", email="setup123@email.com")

    @pytest.mark.unit
    def test_user_serializer(self):
        user = UserFactory.build()
        serializer = UserSerializer(user)

        assert serializer.data

    @pytest.mark.unit
    def test_contest_serializer(self):
        contest = ContestFactory.build()
        serializer = ContestSerializer(contest)

        assert serializer.data

    @pytest.mark.unit
    def test_submission_serializer(self):
        submission = SubmissionFactory.build()
        serializer = SubmissionSerializer(submission)

        assert serializer.data

    @pytest.mark.unit
    def test_comment_serializer(self):
        comment = CommentFactory.build()
        serializer = CommentSerializer(comment)

        assert serializer.data

    @pytest.mark.unit
    def test_vote_serializer(self):
        vote = VoteFactory.build()
        serializer = VoteSerializer(vote)

        assert serializer.data

    @pytest.mark.unit
    def test_result_serializer(self):
        result = ResultFactory.build()
        serializer = ResultSerializer(result)

        assert serializer.data

    @pytest.mark.django_db
    def test_user_serialized_valid_data(self):
        user = UserFactory()
        valid_serialized_data = {
            "email": "new@email.com",
            "date_joined": user.date_joined,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        serializer = UserSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_user_serialized_invalid_data(self):
        user = UserFactory()
        invalid_serialized_data = {
            "email": "user.email",
            "date_joined": user.date_joined,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        serializer = UserSerializer(data=invalid_serialized_data)
        assert not serializer.is_valid()

    @pytest.mark.django_db
    def test_contest_serialized_valid_data(self):
        contest = ContestFactory()
        valid_serialized_data = {
            "date_start": contest.date_start,
            "date_end": contest.date_end,
            "name": contest.name,
            "description": contest.description,
        }

        serializer = ContestSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_contest_serialized_invalid_data(self):
        contest = ContestFactory()
        invalid_serialized_data = {
            "date_start": 321,
            "date_end": 123,
            "name": contest.name,
            "description": contest.description,
        }

        serializer = ContestSerializer(data=invalid_serialized_data)
        assert not serializer.is_valid()

    @pytest.mark.django_db
    def test_submission_serialized_valid_data(self):

        contest = ContestFactory()
        user = UserFactory(first_name="TestSetUp", email="setup123@email.com")
        submission = SubmissionFactory(user=user, contest=contest)

        valid_serialized_data = {
            "user": submission.user.id,
            "contest": submission.contest.id,
            "content": submission.content,
            "description": submission.description,
        }

        serializer = SubmissionSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}
