from django.http import HttpResponse
from rest_framework import generics
from photo.models import Submission, User, Contest
from photo.serializers import SubmissionSerializer, UserSerializer, ContestSerializer, ReventTokenObtainPairSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


def hello(request):
    return HttpResponse("Hello Runtime")


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = []


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


@api_view(http_method_names=["POST"])
def exchange_token(request):
    data = request.data
    # print(json.dumps(data))
    if User.objects.filter(email=data["email"]).exists():
        user = User.objects.get(email=data["email"])
        if data["account"]["provider"] == "google":
            user.google_id = data["account"]["providerAccountId"]

        user.save()
        token = ReventTokenObtainPairSerializer.get_token(user)
        return Response({"access": str(token.access_token), "refresh": str(token), "user": UserSerializer(user).data})
    elif "account" in data:
        if data["account"]["provider"] == "google":
            mapper = map_google_token_to_user_data
        elif data["account"]["provider"] == "linkedin":
            mapper = map_linkedin_token_to_user_data
        user_data = mapper(data)
        # print(json.dumps(user_data))
        user = User.objects.create(**user_data)
        token = ReventTokenObtainPairSerializer.get_token(user)
        return Response({"access": str(token.access_token), "refresh": str(token), "user": UserSerializer(user).data})
    else:
        return Response(
            {"errors": {"token": "Invalid token"}},
            status=HTTP_400_BAD_REQUEST,
        )
