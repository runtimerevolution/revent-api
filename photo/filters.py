from django_filters import rest_framework as filters
from photo.models import Submission


class SubmissionFilter(filters.FilterSet):
    contest = filters.UUIDFilter(field_name="contest__id", lookup_expr="iexact")
    

    class Meta:
        model = Submission
        fields = ["contest"]