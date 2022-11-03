from django.test import Client, TestCase
from rest_framework import status
from photo.serializers import SubmissionSerializer, UserSerializer
from photo.models import Submission, User
from photo.tests.factories import UserFactory, ContestFactory, SubmissionFactory
import uuid
from photo.tests.fixtures import (
    CONTEST_DESCRIPTION,
    CONTEST_NAME,
    SUBMISSION_CONTENT,
    SUBMISSION_DESCRIPTION,
    USER_EMAIL,
    USER_FIRST_NAME,
    USER_LAST_NAME,
    DATE, 
)
import json
from django.core.serializers.json import DjangoJSONEncoder
 

class TestSubmissionsFromContestList(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.contest = ContestFactory()
        self.submission = SubmissionFactory(user=self.user, contest=self.contest)

    def test_list(self):
        qs = Submission.objects.all()
        
        response = self.client.get("/api/submissions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.dumps(SubmissionSerializer(qs, many=True).data, cls=DjangoJSONEncoder),
            json.dumps(response.json()),
        )

    

class TestSubmissionsFromContestListFilter(TestCase):
    
    def test_success(self):
        self.user = UserFactory()
        self.contest = ContestFactory()
        self.submission = SubmissionFactory(user=self.user, contest=self.contest)
        
        qs = Submission.objects.filter(contest__id=self.submission.contest.id)
        
        response = self.client.get(
            f"/api/submissions/?contest={self.submission.contest.id}"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.dumps(SubmissionSerializer(qs, many=True).data, cls=DjangoJSONEncoder),
            json.dumps(response.json()),
        )
    
    def test_failure(self):
        non_existing_uuid = str(uuid.uuid4())
        
        qs = Submission.objects.filter(contest__id=str(uuid.uuid4()))

        response = self.client.get(
            f"/api/submissions/?contest={non_existing_uuid}"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.dumps(SubmissionSerializer(qs, many=True).data, cls=DjangoJSONEncoder),
            json.dumps(response.json()),
        )

class TestSubmissionsFromContestUpdate(TestCase):
    
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.contest = ContestFactory()
        self.contest2 = ContestFactory()
        self.submission = SubmissionFactory(user=self.user, contest=self.contest)
        
    def test_update_put(self):
        response = self.client.put(
            f"/api/submissions/{self.submission.id}/",
            data={
                "user": str(self.user2.id),
                "contest": str(self.contest2.id),
                "url": SUBMISSION_CONTENT,
                "description": SUBMISSION_DESCRIPTION,
            },
            content_type="application/json",
        )
        
        qs = Submission.objects.get(id=self.submission.id)
        
        self.assertEqual(
            json.dumps(SubmissionSerializer(qs).data, cls=DjangoJSONEncoder),
            json.dumps(response.json()),
        )


    def test_update_patch(self):
        response = self.client.patch(
            f"/api/submissions/{self.submission.id}/",
            data={
                "description": SUBMISSION_DESCRIPTION,
            },
            content_type="application/json",
        )
        
        qs = Submission.objects.get(id=self.submission.id)
        
        self.assertEqual(
            json.dumps(SubmissionSerializer(qs).data, cls=DjangoJSONEncoder),
            json.dumps(response.json()),
        )

class TestSubmissionsFromContestDelete(TestCase):
    
    def setUp(self):
        self.user = UserFactory()
        self.contest = ContestFactory()
        self.submission = SubmissionFactory(user=self.user, contest=self.contest)
    
    def test_success(self):
        
        qs = Submission.objects.filter(id=self.submission.id)
        
        response = self.client.delete(
            f"/api/submissions/{self.submission.id}/"
        )
        
        qs = Submission.objects.filter(id=self.submission.id)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            json.dumps(SubmissionSerializer(qs, many=True).data, cls=DjangoJSONEncoder),
            '[]',
        )


