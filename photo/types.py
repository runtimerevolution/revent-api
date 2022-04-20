import strawberry
from . import models
import datetime
import uuid
from strawberry.django import auto


@strawberry.django.type(models.Contest)
class Contest:
    id: auto
    date_start: auto
    date_end: auto
    name: auto
    description: auto


@strawberry.django.type(models.User)
class User:
    id: uuid.UUID
    email: str
    date_joined: str
    first_name: str
    last_name: str


@strawberry.django.type(models.Submission)
class Submission:
    id: uuid.UUID
    user: "User"
    contest: "Contest"
    content: str
    description: str


@strawberry.django.type(models.Comment)
class Comment:
    id: uuid.UUID
    user: "User"
    Submission: "Submission"
    text: str


@strawberry.django.type(models.Vote)
class Vote:
    id: uuid.UUID
    user: "User"
    Submission: "Submission"
    value: int


@strawberry.django.type(models.Result)
class Result:
    id: uuid.UUID
    contest: "Contest"
    submission: "Submission"
    position: int
