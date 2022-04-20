import datetime
import strawberry
from .types import Contest, Comment, Contest
import typing


@strawberry.type
class Query:
    contests: typing.List[Contest]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(self, text: str, user: str, submission: str) -> Contest:

        return Comment(text=text, user=user, submission=submission)

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


schema = strawberry.Schema(query=Query, mutation=Mutation)
