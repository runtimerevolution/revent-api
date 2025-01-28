import pytest
from strawberry.test import GraphQLTestClient
from django.contrib.auth import get_user_model
from photo.models import Contest, ContestSubmission, Picture
from photo.types import WinnerType

@pytest.mark.django_db
def test_winners_query(client: GraphQLTestClient):
    User = get_user_model()
    user = User.objects.create_user(email='testuser@example.com', password='password')
    picture = Picture.objects.create(user=user, name='Test Picture', file='test.jpg')
    contest = Contest.objects.create(title='Test Contest', description='A test contest', prize='Test Prize', voting_draw_end='2023-12-31')
    contest.winners.add(user)
    ContestSubmission.objects.create(contest=contest, picture=picture)

    response = client.query('''
        query {
            winners {
                title
                description
                prize
                voting_draw_end
                winners {
                    name_first
                    name_last
                    submission {
                        picture {
                            name
                            file
                        }
                        number_votes
                    }
                }
            }
        }
    ''')

    assert response.errors is None
    assert response.data['winners'][0]['title'] == 'Test Contest'
    assert response.data['winners'][0]['winners'][0]['name_first'] == user.name_first
    assert response.data['winners'][0]['winners'][0]['submission']['picture']['name'] == 'Test Picture'
