from django.http import HttpResponse
from rest_framework import generics, viewsets
from photo.custom_viewsets import ListRetrieveUpdateCreateViewSet
from photo.models import Submission, User, Contest
from photo.serializers import SubmissionSerializer, UserSerializer, ContestSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from django_filters import rest_framework as filters
from photo.filters import SubmissionFilter

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


class SubmissionViewSet(ListRetrieveUpdateCreateViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubmissionFilter
    # lookup_field = "contest_id"

    # def get_queryset(self):
    #     return Submission.objects.filter(contest=self.id)


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#     pass


@api_view(["GET"])
def submissions_from_contest(request, id):
    contest = Contest.objects.filter(pk=id)
    if(len(contest) == 0):
        return Response([{"detail":"Not found."}])
    submissions = Submission.objects.filter(contest=id)
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)
