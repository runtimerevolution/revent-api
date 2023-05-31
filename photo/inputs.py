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


@strawberry.django.input(User)
class UserInput:
    email: str
    name_first: str
    name_last: str
    profile_picture: "PictureInput"
    profile_picture_updated_at: strawberry.auto
    user_handle: str


@strawberry.django.input(Picture)
class PictureInput:
    user: "UserInput"
    picture_path: str
    likes: List[UserInput]


@strawberry.django.input(PictureComment)
class PictureCommentInput:
    user: "UserInput"
    picture: "PictureInput"
    text: str
    created_at: strawberry.auto


@strawberry.django.input(Collection)
class CollectionInput:
    name: str
    user: "UserInput"
    pictures: List[PictureInput]


@strawberry.django.input(Contest)
class ContestInput:
    title: str
    description: str
    cover_picture: "PictureInput"
    prize: str
    automated_dates: bool
    upload_phase_start: strawberry.auto
    upload_phase_end: strawberry.auto
    voting_phase_end: strawberry.auto
    active: bool
    winners: List[UserInput]
    created_by: "UserInput"


@strawberry.django.input(ContestSubmission)
class ContestSubmissionInput:
    contest: "ContestInput"
    picture: "PictureInput"
    submission_date: strawberry.auto
    votes: List[UserInput]
