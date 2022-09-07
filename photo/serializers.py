from rest_framework import serializers
from photo.models import User, Contest, Submission, Comment, Vote, Result
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "date_joined", "first_name", "last_name"]


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ["id", "date_start", "date_end", "name", "description"]


class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    contest = serializers.PrimaryKeyRelatedField(queryset=Contest.objects.all())

    class Meta:
        model = Submission
        fields = ["id", "user", "contest", "content", "description"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())

    class Meta:
        model = Comment
        fields = ["id", "user", "submission", "text"]


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())

    class Meta:
        model = Vote
        fields = ["id", "user", "submission", "value"]


class ResultSerializer(serializers.ModelSerializer):
    contest = serializers.PrimaryKeyRelatedField(queryset=Contest.objects.all())
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())

    class Meta:
        model = Result
        fields = ["id", "user", "submission", "position"]


class ReventTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token.user = UserSerializer(user).data
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data

        return data
