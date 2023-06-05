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
    profile_picture: str
    profile_picture_updated_at: strawberry.auto
    user_handle: str


@strawberry.django.input(Picture)
class PictureInput:
    user: str
    picture_path: str
    likes: List[str]


@strawberry.django.input(PictureComment)
class PictureCommentInput:
    user: str
    picture: str
    text: str
    created_at: strawberry.auto


@strawberry.django.input(Collection)
class CollectionInput:
    name: str
    user: str
    pictures: List[str]


@strawberry.django.input(Contest)
class ContestInput:
    title: str
    description: str
    cover_picture: str
    prize: str
    automated_dates: bool
    upload_phase_start: strawberry.auto
    upload_phase_end: strawberry.auto
    voting_phase_end: strawberry.auto
    active: bool
    winners: List[str]
    created_by: str


@strawberry.django.input(ContestSubmission)
class ContestSubmissionInput:
    contest: int
    picture: str
    submission_date: strawberry.auto
    votes: List[str]
