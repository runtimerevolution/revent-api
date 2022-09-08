import datetime
from photo.models import User, Contest, Submission, Comment, Vote, Result
import factory
from dateutil.relativedelta import relativedelta


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = "john.doe@test.com"
    date_joined = datetime.datetime.now()
    first_name = "John"
    last_name = "Doe"


class ContestFactory(factory.Factory):
    class Meta:
        model = Contest

    date_start = datetime.datetime.now()
    date_end = datetime.datetime.now() + relativedelta(months=1)
    name = "TestContest"
    description = "Time for a new monthly photo contest"


class SubmissionFactory(factory.Factory):
    class Meta:
        model = Submission

    user = factory.SubFactory(UserFactory)
    contest = factory.SubFactory(ContestFactory)
    content = ""
    description = ""


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    text = "Great picture! Love it!"


class VoteFactory(factory.Factory):
    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    value = 1


class ResultFactory(factory.Factory):
    class Meta:
        model = Result

    contest = factory.SubFactory(ContestFactory)
    submission = factory.SubFactory(SubmissionFactory)
    position = 2
