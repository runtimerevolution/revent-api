import pytest
from strawberry.test import GraphQLTestClient
from django.contrib.auth import get_user_model
from photo.models import Contest, ContestSubmission, Picture
from photo.tests.factories import UserFactory, ContestFactory, ContestSubmissionFactory, PictureFactory

