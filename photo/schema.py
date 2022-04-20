from typing import List

import strawberry
from .types import Contest, Comment
from typing import List


@strawberry.type
class Query:
    contests: List[Contest] = strawberry.django.field()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(self, text: str, user: User, submission: Submission) -> Comment:

        return Comment(text=text, user=user, submission=submission)


schema = strawberry.Schema(query=Query)
