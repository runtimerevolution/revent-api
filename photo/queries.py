import uuid
from typing import List

import strawberry
from django.contrib.postgres.search import SearchVector

from .models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from .types import (
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
    def users(self, user: uuid.UUID = None, email: str = None) -> List[UserType]:
        if user:
            return User.objects.filter(id=user)
        if email:
            return User.objects.filter(email=email)
        return User.objects.all()

    @strawberry.field
    def pictures(self, picture: int = None) -> List[PictureType]:
        if picture:
            return Picture.objects.filter(id=picture)
        return Picture.objects.all()

    @strawberry.field
    def picture_comments(
        self, id: int = None, user_email: str = None, picture_id: int = None
    ) -> List[PictureCommentType]:
        if id:
            return PictureComment.objects.filter(id=id)
        if user_email and picture_id:
            return PictureComment.objects.filter(user=user_email, picture=picture_id)
        elif user_email:
            return PictureComment.objects.filter(user=user_email)
        elif picture_id:
            return PictureComment.objects.filter(picture=picture_id)
        return PictureComment.objects.all()

    @strawberry.field
    def collections(
        self, user_email: str = None, name: str = None, id: int = None
    ) -> List[CollectionType]:
        if id:
            return Collection.objects.filter(id=id)
        if user_email and name:
            return Collection.objects.filter(user__email=user_email, name=name)
        elif user_email:
            return Collection.objects.filter(user__email=user_email)
        elif name:
            return Collection.objects.filter(name=name)
        return Collection.objects.all()

    @strawberry.field
    def contests(self, user_email: str = None, id: int = None) -> List[ContestType]:
        if id:
            return Contest.objects.filter(id=id)
        if user_email:
            return Contest.objects.filter(created_by=user_email)
        return Contest.objects.all()

    @strawberry.field
    def contest_submissions(
        self, user_email: str = None, id: int = None, contest: int = None
    ) -> List[ContestSubmissionType]:
        if id:
            return ContestSubmission.objects.filter(id=id)
        if user_email or contest:
            if user_email:
                return ContestSubmission.objects.filter(picture__user__email=user_email)
            return ContestSubmission.objects.filter(contest__id=contest)
        return ContestSubmission.objects.all()

    @strawberry.field
    def contest_search(self, search: str) -> List[ContestType]:
        contests = Contest.objects.annotate(
            search=SearchVector("title", "description", "prize"),
        ).filter(search=search)

        return contests
