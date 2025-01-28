import pytest
from strawberry.test import GraphQLTestClient
from django.contrib.auth import get_user_model
from photo.models import Contest, ContestSubmission, Picture
from photo.tests.factories import UserFactory, ContestFactory, PictureFactory, ContestSubmissionFactory


@pytest.mark.django_db
def test_winners_query(client: GraphQLTestClient):
    user = UserFactory()
    contest = ContestFactory(created_by=user)
    picture = PictureFactory(user=user)
    submission = ContestSubmissionFactory(contest=contest, picture=picture)
    contest.winners.add(user)

    query = """
    query {
        winners {
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
    data = response.data['winners']

    assert len(data) == 1
    assert data[0]['title'] == contest.title
    assert data[0]['description'] == contest.description
    assert data[0]['prize'] == contest.prize
    assert data[0]['winners'][0]['nameFirst'] == user.name_first
    assert data[0]['winners'][0]['nameLast'] == user.name_last
    assert data[0]['winners'][0]['submission']['picture']['name'] == picture.name
    assert data[0]['winners'][0]['submission']['picture']['file'] == picture.file.url
    assert data[0]['winners'][0]['submission']['numberVotes'] == submission.votes.count()
