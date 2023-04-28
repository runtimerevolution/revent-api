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


@strawberry.django.type(User)
class UserType:
    email: str
    name_first: str
    name_last: str
    profile_picture: "PictureType"
    profile_picture_updated_at: strawberry.auto
    user_handle: str


@strawberry.django.type(Picture)
class PictureType:
    user: "UserType"
    picture_path: str
    likes: List[UserType]


@strawberry.django.type(PictureComment)
class PictureCommentType:
    user: "UserType"
    picture: "PictureType"
    text: str
    created_at: strawberry.auto


@strawberry.django.type(Collection)
class CollectionType:
    name: str
    user: "UserType"
    pictures: List[PictureType]


@strawberry.django.type(Contest)
class ContestType:
    title: str
    description: str
    cover_picture: "PictureType"
    prize: str
    automated_dates: bool
    upload_phase_start: strawberry.auto
    upload_phase_end: strawberry.auto
    voting_phase_end: strawberry.auto
    active: bool
    winners: List[UserType]
    created_by: strawberry.auto


@strawberry.django.type(ContestSubmission)
class ContestSubmissionType:
    contest: str
    picture: "UserType"
    submission_date: strawberry.auto
    votes: List[PictureType]
