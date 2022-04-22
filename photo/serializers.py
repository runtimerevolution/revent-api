from rest_framework import serializers

from photo.models import Comment, Contest, Submission, User, Vote


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User


class ContestSerializer(serializers.Serializer):
    class Meta:
        model = Contest


class SubmissionSerializer(serializers.Serializer):
    class Meta:
        model = Submission


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment


class VoteSerializer(serializers.Serializer):
    class Meta:
        model = Vote
