import datetime
import strawberry

from .types import Contest, Comment, Submission, Vote
from typing import List


@strawberry.type
class Query:
    contests: List[Contest] = strawberry.django.field()

    submissions: List[Submission] = strawberry.django.field()

    comments: List[Comment] = strawberry.django.field()

    votes: List[Vote] = strawberry.django.field()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(self, text: str, user: str, submission: str) -> Comment:

        return Comment(text=text, user=user, submission=submission)

    @strawberry.mutation
    def add_vote(self, value: str, user: str, submission: str) -> Vote:

        return Vote(value=value, user=user, submission=submission)

    @strawberry.mutation
    def add_contest(
        self,
        name: str,
        description: str,
        date_start: datetime.datetime,
        date_end: datetime.datetime,
    ) -> Contest:

        return Contest(
            name=name, description=description, date_start=date_start, date_end=date_end
        )

    @strawberry.mutation
    def add_submission(
        self, content: str, description: str, user: str, contest: str
    ) -> Submission:

        return Submission(
            content=content,
            description=description,
            user=user,
            contest=contest,
        )


@strawberry.type
class User:
    email: str
    first_name: str
    last_name: str
    date_joined: datetime.datetime


schema = strawberry.Schema(query=Query, mutation=Mutation)
