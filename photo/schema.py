from typing import List

import strawberry

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


# Query = strawberry_django.queries(User,  Picture, PictureComment, Collection, Contest, ContestSubmission, types=types)
class Query:
    @strawberry.field
    def users(self, email: str = None) -> List[UserType]:
        if email:
            return User.objects.find(email=email)
        return User.objects.all()

    @strawberry.field
    def pictures(self, path: str = None) -> List[PictureType]:
        if path:
            return Picture.objects.find(picture_path=path)
        return Picture.objects.all()

    @strawberry.field
    def picture_comments(
        self, user_email: str = None, picture_path: str = None
    ) -> List[PictureCommentType]:
        if user_email or picture_path:
            if user_email and picture_path:
                return PictureComment.objects.filter(
                    user=user_email, picture=picture_path
                )
            elif user_email:
                return PictureComment.objects.filter(user=user_email)
            return PictureComment.objects.filter(picture=picture_path)
        return PictureComment.objects.all()

    @strawberry.field
    def collections(self, user_email: str = None) -> List[CollectionType]:
        if user_email:
            return Collection.objects.filter(user=user_email)
        return Collection.objects.all()

    @strawberry.field
    def contests(self, user_email: str = None, id: int = None) -> List[ContestType]:
        if id:
            return Contest.objects.find(id=id)
        if user_email:
            return Contest.objects.filter(user=user_email)
        return Contest.objects.all()

    @strawberry.field
    def contest_submissions(
        self, user_email: str = None, contest: int = None, id: int = None
    ) -> List[ContestSubmissionType]:
        if contest or user_email:
            if contest:
                return ContestSubmission.objects.find(id=contest)
            return ContestSubmission.objects.filter(user=user_email)
        return ContestSubmission.objects.all()


class Mutation:
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
