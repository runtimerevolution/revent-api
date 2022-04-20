import strawberry
from typing import List

from photo.models import Comment
from .types import Contest, User, Submission


@strawberry.type
class Query:
    contests: List[Contest] = strawberry.django.field()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(self, text: str, user: User, submission: Submission) -> Comment:

        return Comment(text=text, user=user, submission=submission)


schema = strawberry.Schema(query=Query, mutation=Mutation)
