from django_filters import rest_framework as filters
from photo.models import Submission


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = ["contest"]