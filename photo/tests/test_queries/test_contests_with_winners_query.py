import pytest
from strawberry.test import GraphQLTestClient
from photo.tests.factories import UserFactory, ContestFactory, ContestSubmissionFactory, PictureFactory

@pytest.mark.django_db
def test_contests_with_winners_query(client: GraphQLTestClient):
    user = UserFactory()
    contest = ContestFactory(created_by=user)
    picture = PictureFactory()
    submission = ContestSubmissionFactory(contest=contest, picture=picture)

    query = """
    query {
        contestsWithWinners {
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

    response = client.query(query)
    assert response.errors is None
    data = response.data['contestsWithWinners']
    assert len(data) == 1
    assert data[0]['title'] == contest.title
    assert data[0]['winners'][0]['submission']['picture']['name'] == picture.name
    assert data[0]['winners'][0]['submission']['numberVotes'] == submission.votes.count()
