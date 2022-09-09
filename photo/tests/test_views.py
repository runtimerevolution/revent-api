import pytest
from django.test import TestCase
from django.urls import reverse
from photo.views import UserViewSet, SubmissionViewSet, ContestViewSet
from photo.models import User, Contest, Submission, Comment, Result, Vote
from factories import UserFactory, ContestFactory, SubmissionFactory, CommentFactory, ResultFactory, VoteFactory
from django.test import Client

# class TestMyView:
#     def test_result_finished(self, rf):
#         url = reverse("users")
#         request = rf.get(reverse("users"))
#         response = UserViewSet.as_view()(request)

#         assert response.status_code == 200


class AuthorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@test.com",
        )

        self.author_test = {"first_name": "Test", "last_name": "LastName"}

        users = User.create_batch(20)
        # login = self.client.login(username="testuser", password="123")

    # def test_list_all_users(self):
    #     response = self.client.get("/users/")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.count(), 20)

    # def test_create_author(self):
    #     # data = {"first_name": "Test", "last_name": "LastName"}
    #     response = self.client.post("/library/author/", data=self.author_test)
    #     self.assertEqual(response.status_code, 201)
