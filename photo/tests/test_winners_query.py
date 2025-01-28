import pytest
from strawberry.test import GraphQLTestClient
from django.contrib.auth import get_user_model
from photo.models import Contest, ContestSubmission, Picture
from photo.schema import schema

User = get_user_model()

@pytest.mark.django_db
def test_winners_query():
    client = GraphQLTestClient(schema)

    # Create test data
    user1 = User.objects.create(email="user1@example.com", name_first="John", name_last="Doe")
    user2 = User.objects.create(email="user2@example.com", name_first="Jane", name_last="Smith")

    picture1 = Picture.objects.create(user=user1, name="Picture 1", file="file1.jpg")
    picture2 = Picture.objects.create(user=user2, name="Picture 2", file="file2.jpg")

    contest = Contest.objects.create(title="Contest 1", description="Description 1", prize="Prize 1")
    contest.winners.add(user1)

    ContestSubmission.objects.create(contest=contest, picture=picture1)
    ContestSubmission.objects.create(contest=contest, picture=picture2)

    # Execute the query
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

    # Validate the response
    assert response.errors is None
    assert response.data == {
        "winners": [
            {
                "title": "Contest 1",
                "description": "Description 1",
                "prize": "Prize 1",
                "votingDrawEnd": None,
                "winners": [
                    {
                        "nameFirst": "John",
                        "nameLast": "Doe",
                        "submission": {
                            "picture": {
                                "name": "Picture 1",
                                "file": "file1.jpg"
                            },
                            "numberVotes": 0
                        }
                    }
                ]
            }
        ]
    }
