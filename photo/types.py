import strawberry
from strawberry.django import auto

from . import models
import uuid


@strawberry.django.type(models.Contest)
class Contest:
    id: auto
    date_start: auto
    date_end: auto
    name: auto
    description: auto


@strawberry.django.type(models.User)
class User:
    id: auto
    email: auto
    date_joined: auto
    first_name: auto
    last_name: auto


@strawberry.django.type(models.Submission)
class Submission:
    id: auto
    user: auto
    contest: auto
    content: auto
    description: auto


@strawberry.django.type(models.Comment)
class Comment:
    id: uuid.UUID
    user: "User"
    Submission: "Submission"
    text: str


@strawberry.django.type(models.Vote)
class Vote:
    id: auto
    user: "User"
    Submission: "Submission"
    value: auto


@strawberry.django.type(models.Result)
class Result:
    id: auto
    contest: "Contest"
    submission: "Submission"
    position: auto
