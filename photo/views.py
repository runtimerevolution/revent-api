from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from photo.models import Submission, User, Contest
from photo.serializers import SubmissionSerializer, UserSerializer, ContestSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

# Create your views here.


def hello(request):
    return HttpResponse("Hello Runtime")


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubmissionList(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class ContestList(generics.ListCreateAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


@api_view(["GET"])
def submissions_from_contest(request, id):
    submissions = Submission.objects.filter(contest=id)
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)
