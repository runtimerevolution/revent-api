import strawberry
from strawberry.schema.config import StrawberryConfig

from photo.queries import Query
from datetime import datetime
from typing import List

import strawberry
from strawberry.schema.config import StrawberryConfig


from .types import (
    CollectionType,
    ContestSubmissionType,
    ContestType,
    PictureCommentType,
    PictureType,
    UserType,
)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(
        self, email: str, firstName: str, lastName: str, userHandle: str = None
    ) -> UserType:
        if not userHandle:
            userHandle = firstName + lastName
        return UserType(
            email=email,
            first_name=firstName,
            last_name=lastName,
            user_handle=userHandle,
        )

    @strawberry.mutation
    def add_picture(self, user: UserType, picturePath: str, likes: List[UserType]):
        return PictureType(user=user, picture_path=picturePath, likes=likes)

    @strawberry.mutation
    def add_picture_comment(self, user: UserType, picturePath: str, text: str):
        return PictureCommentType(
            user=user, picture=picturePath, text=text, created_at=datetime.now()
        )

    @strawberry.mutation
    def add_collection(self, user: UserType, name: str, pictures: List[PictureType]):
        return CollectionType(user=user, name=name, pictures=pictures)

    @strawberry.mutation
    def add_contest(
        self,
        title: str,
        description: str,
        prize: str,
        coverPicture: PictureType,
        createdBy: UserType,
        uploadStart: datetime = datetime.now(),
        uploadEnd: datetime = None,
        votingStart: datetime = None,
        winners: List[UserType] = None,
    ):
        return ContestType(
            title=title,
            description=description,
            prize=prize,
            cover_picture=coverPicture,
            created_by=createdBy,
            upload_phase_start=uploadStart,
            upload_phase_end=uploadEnd,
            voting_phase_start=votingStart,
            winners=winners,
        )

    @strawberry.mutation
    def add_contest_submissioj(
        self, contest: ContestType, picture: PictureType, votes: List[UserType] = None
    ):
        return ContestSubmissionType(
            contest=contest,
            picture=picture,
            votes=votes,
            submission_date=datetime.now(),
        )


schema = strawberry.Schema(
    query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=False)
)
