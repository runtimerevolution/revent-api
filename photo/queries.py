import uuid
from typing import List, Optional

import strawberry
import strawberry_django
from django.contrib.postgres.search import SearchVector
from rest_framework.authentication import TokenAuthentication
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from photo.filters import (
    CollectionFilter,
    ContestFilter,
    ContestSubmissionFilter,
    PictureCommentFilter,
    PictureFilter,
)
from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from photo.permissions import IsAuthenticated
from photo.types import (
    CollectionType,
    ContestSubmissionType,
    ContestType,
    PictureCommentType,
    PictureType,
    UserType,
)
from utils.enums import ContestInternalStates


class Context(BaseContext):
    def user(self) -> User | None:
        if not self.request:
            return None
        authenticator = TokenAuthentication()
        return authenticator.authenticate(self.request)


Info = _Info[Context, RootValueType]


@strawberry.type
class Query:
    @strawberry.field
    def users(self, user: uuid.UUID = None) -> List[UserType]:
        return User.objects.filter(id=user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_authenticated_user(self, info: Info) -> UserType | None:
        return info.context.user()

    @strawberry.field
    def pictures(
        self, filters: Optional[PictureFilter] = strawberry.UNSET
    ) -> List[PictureType]:
        queryset = Picture.objects.all()
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def picture_comments(
        self, filters: Optional[PictureCommentFilter] = strawberry.UNSET
    ) -> List[PictureCommentType]:
        queryset = PictureComment.objects.all()
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def collections(
        self, filters: Optional[CollectionFilter] = strawberry.UNSET
    ) -> List[CollectionType]:
        queryset = Collection.objects.all()
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def contests(
        self, filters: Optional[ContestFilter] = strawberry.UNSET
    ) -> List[ContestType]:
        queryset = Contest.objects.all()
        if getattr(filters, "search", strawberry.UNSET):
            queryset = Contest.objects.annotate(
                search=SearchVector("title", "description", "prize"),
            ).filter(search__icontains=filters.search)
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def contest_submissions(
        self, filters: Optional[ContestSubmissionFilter] = strawberry.UNSET
    ) -> List[ContestSubmissionType]:
        queryset = []
        if filters.draw and filters.contest:
            contest = Contest.objects.filter(
                id=filters.contest.id, internal_status=ContestInternalStates.DRAW
            ).first()
            contest_winners = [user.id for user in contest.winners.all()]
            queryset = ContestSubmission.objects.filter(
                picture__user__id__in=contest_winners
            )
        else:
            queryset = ContestSubmission.objects.all()
        return strawberry_django.filters.apply(filters, queryset)
