import random

import factory
import pytz

from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name_first = factory.Faker("first_name")
    name_last = factory.Faker("last_name")
    user_handle = factory.Faker("name")
    profile_picture = factory.RelatedFactory(
        "tests.factories.PictureFactory", "user", likes=None
    )
    profile_picture_updated_at = factory.Faker("date_time")


class PictureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Picture

    user = factory.SubFactory(UserFactory)
    picture_path = factory.Faker("url")
    likes = factory.RelatedFactoryList(
        "tests.factories.UserFactory",
        profile_picture=None,
        size=lambda: random.randint(0, 5),
    )


class PictureCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PictureComment

    user = factory.SubFactory(UserFactory)
    picture = factory.SubFactory(PictureFactory)
    text = factory.Faker("sentence")
    created_at = factory.Faker("date_time", tzinfo=pytz.UTC)


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    name = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    pictures = factory.RelatedFactoryList(
        PictureFactory, user=user, size=lambda: random.randint(0, 10)
    )


class ContestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contest

    title = factory.Faker("name")
    description = factory.Faker("sentence")
    cover_picture = factory.SubFactory(PictureFactory)
    prize = factory.Faker("sentence")
    automated_dates = factory.LazyAttribute(True)
    upload_phase_start = factory.Faker("date_time", tzinfo=pytz.UTC)
    upload_phase_end = factory.Faker("date_time", tzinfo=pytz.UTC)
    voting_phase_end = factory.Faker("date_time", tzinfo=pytz.UTC)
    active = factory.LazyAttribute(True)
    winners = factory.RelatedFactoryList(UserFactory, size=lambda: random.randint(0, 3))
    created_by = factory.LazyAttribute(factory.SelfAttribute("..cover_picture.user"))


class ContestSubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContestSubmission

    contest = factory.SubFactory(ContestFactory)
    picture = factory.SubFactory(PictureFactory)
    submissionDate = factory.Faker("date_time", tzinfo=pytz.UTC)
    votes = factory.RelatedFactoryList(UserFactory, size=lambda: random.randint(0, 10))
