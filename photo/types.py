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
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.django.type(Picture)
class PictureType:
    id: int
    user: "UserType"
    name: str
    file: str
    likes: List[UserType]
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.django.type(PictureComment)
class PictureCommentType:
    id: int
    user: "UserType"
    picture: "PictureType"
    text: str
    created_at: strawberry.auto

    updated_at: strawberry.auto

@strawberry.django.type(Collection)
class CollectionType:
    id: int
    name: str
    user: "UserType"
    pictures: List[PictureType]
    created_at: strawberry.auto
    updated_at: strawberry.auto


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
    voting_draw_end: strawberry.auto
    internal_status: str
    winners: List[UserType]
    created_by: "UserType"
    status: str
    created_at: strawberry.auto
    updated_at: strawberry.auto

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
    contest: ContestType
    picture: PictureType
    submission_date: strawberry.auto
    votes: List[UserType]
    created_at: strawberry.auto
    updated_at: strawberry.auto


@strawberry.type
class AddVoteMutationResponse:
    success: bool
    results: ContestSubmissionType | None
    errors: str


@strawberry.type
class CreatePictureMutationResponse:
    success: bool
    results: PictureType
    errors: str


@strawberry.type
class CreateContestSubmissiomMutationResponse:
    success: bool
    results: ContestSubmissionType
    errors: str


@strawberry.type
class AddLikeMutationResponse:
    success: bool
    results: PictureType
    errors: str


@strawberry.type
class CollectionAddPictureMutationResponse:
    success: bool
    results: CollectionType
    errors: str


@strawberry.type
class CloseContestMutationResponse:
    success: bool
    results: ContestType
    errors: str
