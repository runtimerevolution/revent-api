from datetime import timezone
from photo.models import User, Contest, Submission, Comment, Vote, Result
import factory
from dateutil.relativedelta import relativedelta


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = "john.doe@test.com"
    date_joined = timezone.now
    first_name = "John"
    last_name = "Doe"


class ContestFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contest

    date_start = timezone.now
    date_end = timezone.now + relativedelta(months=1)
    name = "May Madness Contest"
    description = "Time for a new monthly photo contest"


class SubmissionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Submission

    user = factory.SubFactory(UserFactory)
    contest = factory.SubFactory(ContestFactory)
    content = ""
    description = ""


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    text = "Great picture! Love it!"


class VoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    value = 1


class ResultFactory(factory.DjangoModelFactory):
    class Meta:
        model = Result

    contest = factory.SubFactory(ContestFactory)
    submission = factory.SubFactory(SubmissionFactory)
    position = 1
