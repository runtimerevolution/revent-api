import uuid
from typing import List, Optional

import strawberry
import strawberry_django
from django.contrib.postgres.search import SearchVector

from photo.filters import PictureFilter
from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from photo.types import (
    CollectionType,
    ContestSubmissionType,
    ContestType,
    PictureCommentType,
    PictureType,
    UserType,
)


@strawberry.type
class Query:
    @strawberry.field
    def users(self, user: uuid.UUID = None) -> List[UserType]:
        return User.objects.filter(id=user)

    @strawberry.field
    def pictures(
        self, filters: Optional[PictureFilter] = strawberry.UNSET
    ) -> List[PictureType]:
        queryset = Picture.objects.all()
        queryset = strawberry_django.filters.apply(filters, queryset)
        return queryset.order_by("pk").values_list("pk", flat=True)

    @strawberry.field
    def picture_comments(
        self, id: int = None, user: uuid.UUID = None, picture_id: int = None
    ) -> List[PictureCommentType]:
        if id:
            return PictureComment.objects.filter(id=id)
        if user and picture_id:
            return PictureComment.objects.filter(user=user, picture=picture_id)
        elif user:
            return PictureComment.objects.filter(user=user)
        elif picture_id:
            return PictureComment.objects.filter(picture=picture_id)
        return PictureComment.objects.all()

    @strawberry.field
    def collections(
        self, user: uuid.UUID = None, name: str = None, id: int = None
    ) -> List[CollectionType]:
        if id:
            return Collection.objects.filter(id=id)
        if user and name:
            return Collection.objects.filter(user=user, name=name)
        elif user:
            return Collection.objects.filter(user=user)
        elif name:
            return Collection.objects.filter(name=name)
        return Collection.objects.all()

    @strawberry.field
    def contests(self, user: uuid.UUID = None, id: int = None) -> List[ContestType]:
        if id:
            return Contest.objects.filter(id=id)
        if user:
            return Contest.objects.filter(created_by=user)
        return Contest.objects.all()

    @strawberry.field
    def contest_submissions(
        self, user: uuid.UUID = None, id: int = None, contest: int = None
    ) -> List[ContestSubmissionType]:
        if id:
            return ContestSubmission.objects.filter(id=id)
        if user or contest:
            if user:
                return ContestSubmission.objects.filter(picture__user=user)
            return ContestSubmission.objects.filter(contest__id=contest)
        return ContestSubmission.objects.all()

    @strawberry.field
    def contest_search(self, search: str) -> List[ContestType]:
        contests = Contest.objects.annotate(
            search=SearchVector("title", "description", "prize"),
        ).filter(search=search)

        return contests
