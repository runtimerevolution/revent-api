import strawberry
from . import models
import datetime


@strawberry.django.type(models.Contest)
class Contest:
    date_start: datetime.datetime
    date_end: datetime.datetime
    name: str
    description: str


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
