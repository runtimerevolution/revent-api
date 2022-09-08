import pytest
from photo.models import User, Contest, Submission, Vote, Result
from factories import (
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


class TestUserSerializer:
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
