import datetime
from typing import List

import strawberry

from .models import Comment as CommentModel
from .models import Contest as ContestModel
from .models import Submission as SubmissionModel
from .models import User as UserModel
from .models import Vote as VoteModel
from .types import Comment, Contest, Submission, Vote


@strawberry.type
class Query:
    contests: List[Contest] = strawberry.django.field()

    submissions: List[Submission] = strawberry.django.field()

    comments: List[Comment] = strawberry.django.field()

    votes: List[Vote] = strawberry.django.field()

    @strawberry.field
    def get_contest_by_id(self, id: strawberry.ID) -> Contest:
        return ContestModel.objects.filter(pk=id).first()

    @strawberry.field
    def get_submissions_by_contest_id(self, id: strawberry.ID) -> List[Submission]:
        return SubmissionModel.objects.filter(contest=id)

    @strawberry.field
    def get_comments_by_submission_id(self, id: strawberry.ID) -> List[Comment]:
        return CommentModel.objects.filter(submission=id)

    @strawberry.field
    def get_votes_by_submission_id(self, id: strawberry.ID) -> List[Vote]:
        return VoteModel.objects.filter(submission=id)

    @strawberry.field
    def get_current_contests(self) -> List[Contest]:
        return ContestModel.objects.filter(
            date_start__lte=datetime.datetime.now(),
            date_end__gte=datetime.datetime.now(),
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(
        self, text: str, user_id: strawberry.ID, submission_id: strawberry.ID
    ) -> Comment:
        user = UserModel.objects.filter(pk=user_id).first()
        submission = SubmissionModel.objects.filter(pk=submission_id).first()
        comment = CommentModel(text=text, user=user, submission=submission)
        comment.save()

        return comment

    @strawberry.mutation
    def add_vote(
        self, value: str, user_id: strawberry.ID, submission_id: strawberry.ID
    ) -> Vote:
        user = UserModel.objects.filter(pk=user_id).first()
        submission = SubmissionModel.objects.filter(pk=submission_id).first()
        vote = VoteModel(value=value, user=user, submission=submission)
        vote.save()
        return vote

    @strawberry.mutation
    def add_contest(
        self,
        name: str,
        description: str,
        date_start: datetime.datetime,
        date_end: datetime.datetime,
    ) -> Contest:

        contest = ContestModel(
            name=name, description=description, date_start=date_start, date_end=date_end
        )
        contest.save()
        return contest

    @strawberry.mutation
    def add_submission(
        self,
        content: str,
        description: str,
        user_id: strawberry.ID,
        contest_id: strawberry.ID,
    ) -> Submission:

        user = UserModel.objects.filter(pk=user_id).first()
        contest = ContestModel.objects.filter(pk=contest_id).first()

        submission = SubmissionModel(
            content=content,
            description=description,
            user=user,
            contest=contest,
        )
        submission.save()
        return submission

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
