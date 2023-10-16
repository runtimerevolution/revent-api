import uuid

import strawberry

from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)


@strawberry.django.filters.filter(User, lookups=True)
class UserFilter:
    id: uuid.UUID


@strawberry.django.filters.filter(Picture, lookups=True)
class PictureFilter:
    id: int
    user: UserFilter


@strawberry.django.filters.filter(PictureComment, lookups=True)
class PictureCommentFilter:
    id: int
    picture: PictureFilter


@strawberry.django.filters.filter(Collection, lookups=True)
class CollectionFilter:
    id: int
    name: str
    user: UserFilter


@strawberry.django.filters.filter(Contest, lookups=True)
class ContestFilter:
    id: int
    created_by: UserFilter
    status: str
    search: str
    upload_phase_start: strawberry.auto


@strawberry.django.filters.filter(ContestSubmission, lookups=True)
class ContestSubmissionFilter:
    id: int
    picture: PictureFilter
    contest: ContestFilter
