from django.test import TestCase
from strawberry.test import GraphQLTestClient
from photo.schema import schema
from photo.models import Contest, User, ContestSubmission, Picture

class WinnersViewTest(TestCase):
    def setUp(self):
        self.client = GraphQLTestClient(schema)
        self.user = User.objects.create(name_first="John", name_last="Doe")
        self.picture = Picture.objects.create(name="Sample Picture", file="sample.jpg", user=self.user)
        self.contest = Contest.objects.create(title="Sample Contest", description="A sample contest", prize="Sample Prize", voting_draw_end="2023-12-31")
        self.contest.winners.add(self.user)
        ContestSubmission.objects.create(contest=self.contest, picture=self.picture)

    def test_winners_view(self):
        response = self.client.query("""
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
        """)

        self.assertIsNone(response.errors)
        data = response.data['winners'][0]
        self.assertEqual(data['title'], "Sample Contest")
        self.assertEqual(data['description'], "A sample contest")
        self.assertEqual(data['prize'], "Sample Prize")
        self.assertEqual(data['winners'][0]['name_first'], "John")
        self.assertEqual(data['winners'][0]['name_last'], "Doe")
        self.assertEqual(data['winners'][0]['submission']['picture']['name'], "Sample Picture")
        self.assertEqual(data['winners'][0]['submission']['picture']['file'], "sample.jpg")
        self.assertEqual(data['winners'][0]['submission']['number_votes'], 0)
