import uuid
from typing import List

import strawberry
from django.utils import timezone

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
    id: uuid.UUID
    email: str
    name_first: str
    name_last: str
    profile_picture: "PictureType"
    profile_picture_updated_at: strawberry.auto
    user_handle: str


@strawberry.django.type(Picture)
class PictureType:
    id: int
    user: "UserType"
    name: str
    file: str
    likes: List[UserType]


@strawberry.django.type(PictureComment)
class PictureCommentType:
    id: int
    user: "UserType"
    picture: "PictureType"
    text: str
    created_at: strawberry.auto


@strawberry.django.type(Collection)
class CollectionType:
    id: int
    name: str
    user: "UserType"
    pictures: List[PictureType]


@strawberry.django.type(Contest)
class ContestType:
    id: int
    title: str
    description: str
    cover_picture: "PictureType"
    prize: str
    automated_dates: bool
    upload_phase_start: strawberry.auto
    upload_phase_end: strawberry.auto
    voting_phase_end: strawberry.auto
    winners: List[UserType]
    created_by: "UserType"
    status: str

    @strawberry.field
    def status(self) -> str:
        currentTime = timezone.now()
        if self.upload_phase_start > currentTime:
            return "scheduled"
        elif self.upload_phase_end is None:
            return "open"
        elif self.upload_phase_end > currentTime:
            return "open"
        elif self.voting_phase_end is None:
            return "voting"
        elif self.voting_phase_end > currentTime:
            return "voting"
        else:
            return "closed"


@strawberry.django.type(ContestSubmission)
class ContestSubmissionType:
    id: int
    contest: "ContestType"
    picture: "PictureType"
    submission_date: strawberry.auto
    votes: List[UserType]


@strawberry.type
class AddVoteMutationResponse:
    success: bool
    results: ContestSubmissionType
    error: str


@strawberry.type
class CloseContestMutationResponse:
    success: bool
    results: ContestType
    error: str
