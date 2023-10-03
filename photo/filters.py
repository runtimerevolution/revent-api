import django_filters
import strawberry_django

from photo.models import Picture


@strawberry_django.filter
class PictureFilter(django_filters.FilterSet):
    class Meta:
        model = Picture
        fields = ["id", "user"]
