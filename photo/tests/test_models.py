import pytest
from photo.models import User, Contest, Submission, Vote, Result


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create(first_name="john", email="lennon@thebeatles.com")
    assert User.objects.count() == 1
    assert user.first_name == "john"
    assert user.email == "lennon@thebeatles.com"


@pytest.mark.django_db
def test_create_contest():
    contest = Contest.objects.create(name="TestContest", date_end="2022-09-28T15:11:16Z")
    assert Contest.objects.count() == 1
    assert contest.name == "TestContest"


@pytest.mark.django_db
def test_submission_create():
    user = User.objects.create(first_name="john", email="lennon@thebeatles.com")
    contest = Contest.objects.create(name="TestContest", date_end="2022-09-28T15:11:16Z")
    submission = Submission.objects.create(user=user, contest=contest)
    assert Submission.objects.count() == 1
    assert submission.user.first_name == "john"
    assert submission.contest.name == "TestContest"


@pytest.mark.django_db
def test_vote():
    user = User.objects.create(first_name="john", email="lennon@thebeatles.com")
    contest = Contest.objects.create(name="TestContest", date_end="2022-09-28T15:11:16Z")
    submission = Submission.objects.create(user=user, contest=contest)
    vote = Vote.objects.create(user=user, submission=submission, value=1)
    assert Submission.objects.count() == 1
    assert vote.user.first_name == "john"
    assert vote.submission.user == user
    assert vote.value == 1


@pytest.mark.django_db
def test_result():
    user = User.objects.create(first_name="john", email="lennon@thebeatles.com")
    contest = Contest.objects.create(name="TestContest", date_end="2022-09-28T15:11:16Z")
    submission = Submission.objects.create(user=user, contest=contest)
    result = Result.objects.create(contest=contest, submission=submission, position=2)
    assert Result.objects.count() == 1
    assert result.contest == contest
    assert result.submission.user == user
    assert result.position == 2
