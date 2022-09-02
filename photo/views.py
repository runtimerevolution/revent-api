from django.http import HttpResponse
from rest_framework import generics
from photo.models import Submission, User, Contest
from photo.serializers import SubmissionSerializer, UserSerializer, ContestSerializer

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
