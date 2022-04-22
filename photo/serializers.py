from rest_framework import serializers

from photo.models import Comment, Contest, Submission, User


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

