import strawberry

from photo.models import Picture


@strawberry.django.filters.filter(Picture, lookups=True)
class PictureFilter:
    id: int
