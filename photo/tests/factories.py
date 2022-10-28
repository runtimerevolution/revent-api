import datetime
from photo.models import User, Contest, Submission, Comment, Vote, Result
import factory
from dateutil.relativedelta import relativedelta


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = (
            "email",
            "date_joined",
            "first_name",
            "last_name"
        )

    email = factory.Faker("ascii_company_email")
    date_joined = datetime.datetime.now()
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class ContestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contest
        django_get_or_create = (
            "date_start",
            "date_end",
            "name",
            "description",
        )

    date_start = datetime.datetime.now()
    date_end = datetime.datetime.now() + relativedelta(months=1)
    name = factory.Faker("sentence", nb_words=3, variable_nb_words=True)
    description = factory.Faker("sentence", nb_words=10, variable_nb_words=True)


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission
        django_get_or_create = (
            "user",
            "contest",
            "content",
            "description",
        )

    user = factory.SubFactory(UserFactory)
    contest = factory.SubFactory(ContestFactory)
    url = factory.django.ImageField(color=factory.Faker("color"))
    description = factory.Faker("sentence", nb_words=10, variable_nb_words=True)


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)
    text = factory.Faker("sentence", nb_words=5, variable_nb_words=True)


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
