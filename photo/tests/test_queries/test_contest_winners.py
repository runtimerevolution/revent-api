import pytest
from django.utils import timezone

from photo.models import Contest, ContestSubmission, Picture, User
from photo.tests.test_queries.graphql_queries import CONTEST_WINNERS_QUERY
from utils.enums import ContestInternalStates

pytestmark = pytest.mark.django_db


def test_contest_winners_query(client):
    # Create test users
    user1 = User.objects.create(
        email="user1@test.com",
        name_first="User",
        name_last="One"
    )
    user2 = User.objects.create(
        email="user2@test.com",
        name_first="User",
        name_last="Two"
    )

    # Create test pictures
    picture1 = Picture.objects.create(
        user=user1,
        name="Picture 1",
        file="test1.jpg"
    )
    picture2 = Picture.objects.create(
        user=user2,
        name="Picture 2",
        file="test2.jpg"
    )

    # Create test contests
    contest1 = Contest.objects.create(
        title="Contest 1",
        description="Test Contest 1",
        prize="Prize 1",
        voting_draw_end=timezone.now(),
        internal_status=ContestInternalStates.CLOSED
    )
    contest2 = Contest.objects.create(
        title="Contest 2",
        description="Test Contest 2",
        prize="Prize 2",
        voting_draw_end=timezone.now() + timezone.timedelta(days=1),
        internal_status=ContestInternalStates.CLOSED
    )

    # Create submissions
    submission1 = ContestSubmission.objects.create(
        contest=contest1,
        picture=picture1
    )
    submission2 = ContestSubmission.objects.create(
        contest=contest2,
        picture=picture2
    )

    # Add votes to submissions
    submission1.votes.add(user2)
    submission2.votes.add(user1)

    # Add winners to contests
    contest1.winners.add(user1)
    contest2.winners.add(user2)

    # Execute query
    response = client.post(
        "/graphql/",
        {"query": CONTEST_WINNERS_QUERY},
        content_type="application/json",
    )

    # Check response
    assert response.status_code == 200
    data = response.json()["data"]["contestWinners"]
    assert len(data) == 2

    # Check first contest
    assert data[0]["title"] == "Contest 1"
    assert data[0]["description"] == "Test Contest 1"
    assert data[0]["prize"] == "Prize 1"
    assert len(data[0]["winners"]) == 1
    assert data[0]["winners"][0]["name_first"] == "User"
    assert data[0]["winners"][0]["name_last"] == "One"
    assert data[0]["winners"][0]["submission"]["picture"]["name"] == "Picture 1"
    assert data[0]["winners"][0]["submission"]["picture"]["file"] == "test1.jpg"
    assert data[0]["winners"][0]["submission"]["number_votes"] == 1

    # Check second contest
    assert data[1]["title"] == "Contest 2"
    assert data[1]["description"] == "Test Contest 2"
    assert data[1]["prize"] == "Prize 2"
    assert len(data[1]["winners"]) == 1
    assert data[1]["winners"][0]["name_first"] == "User"
    assert data[1]["winners"][0]["name_last"] == "Two"
    assert data[1]["winners"][0]["submission"]["picture"]["name"] == "Picture 2"
    assert data[1]["winners"][0]["submission"]["picture"]["file"] == "test2.jpg"
    assert data[1]["winners"][0]["submission"]["number_votes"] == 1
