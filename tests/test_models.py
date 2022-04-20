import pytest
from .factories import (
    UserFactory,
    ContestFactory,
    SubmissionFactory,
    CommentFactory,
    VoteFactory,
    ResultFactory,
)


@pytest.mark.django_db
def test_user_model():
    user = UserFactory()
    assert user.email == "john.doe@test.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"


@pytest.mark.django_db
def test_contest_model():
    contest = ContestFactory()
    assert contest.name == "May Madness Contest"
    assert contest.description == "Time for a new monthly photo contest"
    assert contest.date_start.month != contest.date_end.month


@pytest.mark.django_db
def test_submission_model():
    contest = ContestFactory()
    submission = SubmissionFactory(contest=contest)

    assert submission.contest == contest
    assert submission.description == ""


@pytest.mark.django_db
def test_comment_model():
    user = UserFactory()
    submission = SubmissionFactory()
    comment = CommentFactory(user=user, submission=submission)

    assert comment.user == user
    assert comment.submission == submission
    assert comment.text == "Great picture! Love it!"


@pytest.mark.django_db
def test_vote_model():
    user = UserFactory()
    submission = SubmissionFactory()
    vote = VoteFactory(user=user, submission=submission)

    assert vote.user == user
    assert vote.submission == submission
    assert vote.value == 1


@pytest.mark.django_db
def test_result_model():
    contest = ContestFactory()
    submission = SubmissionFactory(contest=contest)
    result = ResultFactory(submission=submission, contest=contest)

    assert result.contest == contest
    assert result.submission == submission
    assert result.position == 1
