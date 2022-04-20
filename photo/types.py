import datetime

import strawberry
from strawberry.django import auto

from . import models


@strawberry.django.type(models.Contest)
class Contest:
    date_start: auto
    date_end: auto
    name: auto
    description: auto


@strawberry.django.type(models.User)
class User:
    email: str
    date_joined: str
    first_name: str
    last_name: str


@strawberry.django.type(models.Submission)
class Submission:
    user: "User"
    contest: "Contest"
    content: str
    description: str


@strawberry.django.type(models.Comment)
class Comment:
    user: "User"
    Submission: "Submission"
    text: str


@strawberry.django.type(models.Vote)
class Vote:
    user: "User"
    Submission: "Submission"
    value: int


@strawberry.django.type(models.Result)
class Result:
    contest: "Contest"
    submission: "Submission"
    position: int
