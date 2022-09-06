from django.http import HttpResponse
from rest_framework import generics
from photo.models import Submission, User, Contest
from photo.serializers import SubmissionSerializer, UserSerializer, ContestSerializer

from rest_framework.decorators import api_view
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
def current_user(request):
    if request.user.is_authenticated:
        # && request.user.is_contest_manager:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response("No authenticated user.")
