from django.http import HttpResponse
from rest_framework import generics, viewsets
from photo.models import Submission, User, Contest
from photo.serializers import SubmissionSerializer, UserSerializer, ContestSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response


def hello(request):
    return HttpResponse("Hello Runtime")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["GET"], url_path="authenticated", detail=False)
    def current_user(self, request):
        if request.user.is_authenticated:
            # && request.user.is_contest_manager:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        return Response("No authenticated user.")


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


@api_view(["GET"])
def submissions_from_contest(request, id):
    submissions = Submission.objects.filter(contest=id)
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)
