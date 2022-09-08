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


@pytest.mark.django_db
def test_create_user():
    user = UserFactory()
    assert user.first_name == "John"
    assert user.email == "john.doe@test.com"


@pytest.mark.django_db
def test_contest_model():
    contest = ContestFactory()
    assert contest.name == "TestContest"
    assert contest.description == "Time for a new monthly photo contest"
    assert contest.date_start.month != contest.date_end.month


@pytest.mark.django_db
def test_create_submission():
    user = UserFactory()
    contest = ContestFactory()
    submission = SubmissionFactory(user=user, contest=contest)
    assert submission.user.first_name == "John"
    assert submission.contest.name == "TestContest"


@pytest.mark.django_db
def test_create_vote():
    user = UserFactory()
    contest = ContestFactory()
    submission = SubmissionFactory(user=user, contest=contest)
    vote = VoteFactory(user=user, submission=submission, value=1)
    assert vote.user.first_name == "John"
    assert vote.submission.user == user
    assert vote.value == 1


@pytest.mark.django_db
def test_create_result():
    user = UserFactory()
    contest = ContestFactory()
    submission = SubmissionFactory(user=user, contest=contest)
    result = ResultFactory(contest=contest, submission=submission, position=2)
    assert result.contest == contest
    assert result.submission.user == user
    assert result.position == 2
