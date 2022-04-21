import datetime
import strawberry
from .types import Contest, Comment, Submission, Vote
from typing import List
from .models import Comment as CommentModel, Submission as SubmissionModel


@strawberry.type
class Query:
    contests: List[Contest] = strawberry.django.field()

    submissions: List[Submission] = strawberry.django.field()

    comments: List[Comment] = strawberry.django.field()

    votes: List[Vote] = strawberry.django.field()


@strawberry.input
class UserInput:
    email: str
    first_name: str
    last_name: str
    date_joined: datetime.datetime


@strawberry.input
class ContestInput:
    name: str
    description: str
    date_start: datetime.datetime
    date_end: datetime.datetime


@strawberry.input
class SubmissionInput:
    user: UserInput
    contest: ContestInput
    content: str
    description: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(
        self, text: str, user: UserInput, submission: SubmissionInput
    ) -> Comment:

        return Comment(text=text, user=user, submission=submission)

    @strawberry.mutation
    def add_vote(
        self, value: str, user: UserInput, submission: SubmissionInput
    ) -> Vote:

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
        self, content: str, description: str, user: UserInput, contest: ContestInput
    ) -> Submission:

        return Submission(
            content=content,
            description=description,
            user=user,
            contest=contest,
        )

    @strawberry.mutation
    def update_submission(
        self, id: strawberry.ID, content: str, description: str
    ) -> Submission:
        obj = SubmissionModel.objects.get(pk=id)
        obj.content = content
        obj.description = description
        obj.save()

        return obj

    @strawberry.mutation
    def update_comment(self, id: strawberry.ID, text: str, user: UserInput) -> Comment:
        obj = CommentModel.objects.get(pk=id)
        obj.text = text
        obj.save()

        return obj


schema = strawberry.Schema(query=Query, mutation=Mutation)
