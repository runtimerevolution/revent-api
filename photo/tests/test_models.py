import pytest
import json
from photo.models import User, Contest, Submission, Vote, Result
from ..serializers import SubmissionSerializer, UserSerializer
from .factories import (
    UserFactory,
    ContestFactory,
    SubmissionFactory,
    CommentFactory,
    VoteFactory,
    ResultFactory,
)
from django.core.serializers.json import DjangoJSONEncoder

@pytest.mark.django_db
def test_create_user():
    user = UserFactory()
    
    qs = User.objects.get(id=user.id)
    
    assert user.first_name == qs.first_name
    assert user.email == qs.email
    assert user.last_name == qs.last_name


@pytest.mark.django_db
def test_contest_model():
    contest = ContestFactory()
    
    qs = Contest.objects.get(id=contest.id)
     
    assert contest.name == qs.name
    assert contest.description == qs.description
    assert contest.date_start.month != contest.date_end.month


@pytest.mark.django_db
def test_create_submission():
    user = UserFactory()
    contest = ContestFactory()
    submission = SubmissionFactory(user=user, contest=contest)
    
    qs = Submission.objects.get(id=submission.id)
    
    assert submission.user == qs.user
    assert submission.contest == qs.contest


@pytest.mark.django_db
def test_create_vote():
    user = UserFactory()
    contest = ContestFactory()
    submission = SubmissionFactory(user=user, contest=contest)
    vote = VoteFactory(user=user, submission=submission, value=1)
    assert vote.user.first_name == user.first_name
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
