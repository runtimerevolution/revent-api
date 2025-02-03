import pytest
from django.utils import timezone

from photo.models import Contest, ContestSubmission, Picture, User
from photo.tests.factories import (
    ContestFactory,
    ContestSubmissionFactory,
    PictureFactory,
    UserFactory,
)


@pytest.mark.django_db
def test_contest_winners_query(client):
    # Create test data
    user1 = UserFactory(name_first="John", name_last="Doe")
    user2 = UserFactory(name_first="Jane", name_last="Smith")

    contest1 = ContestFactory(
        title="Contest 1",
        description="First contest",
        prize="Prize 1",
        voting_draw_end=timezone.now()
    )
    contest1.winners.add(user1)

    contest2 = ContestFactory(
        title="Contest 2",
        description="Second contest",
        prize="Prize 2",
        voting_draw_end=timezone.now() + timezone.timedelta(days=1)
    )
    contest2.winners.add(user1, user2)

    # Create submissions for winners
    picture1 = PictureFactory(user=user1, name="Picture 1")
    submission1 = ContestSubmissionFactory(contest=contest1, picture=picture1)
    # Add some votes
    submission1.votes.add(UserFactory(), UserFactory(), UserFactory())

    picture2 = PictureFactory(user=user1, name="Picture 2")
    submission2 = ContestSubmissionFactory(contest=contest2, picture=picture2)
    submission2.votes.add(UserFactory(), UserFactory())

    picture3 = PictureFactory(user=user2, name="Picture 3")
    submission3 = ContestSubmissionFactory(contest=contest2, picture=picture3)
    submission3.votes.add(UserFactory(), UserFactory(), UserFactory(), UserFactory())

    # Execute query
    query = """
    query {
        contestWinners {
            title
            description
            prize
            votingDrawEnd
            winners {
                nameFirst
                nameLast
                submission {
                    picture {
                        name
                        file
                    }
                    numberVotes
                }
            }
        }
    }
    """

    response = client.execute(query)
    data = response.data["contestWinners"]

    # Verify response
    assert len(data) == 2

    # Verify first contest
    assert data[0]["title"] == "Contest 1"
    assert data[0]["description"] == "First contest"
    assert data[0]["prize"] == "Prize 1"
    assert len(data[0]["winners"]) == 1
    assert data[0]["winners"][0]["nameFirst"] == "John"
    assert data[0]["winners"][0]["nameLast"] == "Doe"
    assert data[0]["winners"][0]["submission"]["picture"]["name"] == "Picture 1"
    assert data[0]["winners"][0]["submission"]["numberVotes"] == 3

    # Verify second contest
    assert data[1]["title"] == "Contest 2"
    assert data[1]["description"] == "Second contest"
    assert data[1]["prize"] == "Prize 2"
    assert len(data[1]["winners"]) == 2

    # Winners should be present in response
    winner_names = {
        (winner["nameFirst"], winner["nameLast"])
        for winner in data[1]["winners"]
    }
    assert winner_names == {("John", "Doe"), ("Jane", "Smith")}

    # Verify vote counts
    vote_counts = {
        winner["submission"]["numberVotes"]
        for winner in data[1]["winners"]
    }
    assert vote_counts == {2, 4}
