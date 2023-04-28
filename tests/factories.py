import datetime
import random

import factory

from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name_first = factory.Faker("first_name")
    name_last = factory.Faker("last_name")
    user_handle = name_first + name_last
    profile_picture = factory.RelatedFactory("PictureFactory", "user")
    profile_picture_updated_at = factory.LazyAttribute(datetime.datetime.now)


class PictureFactory(factory.Factory):
    class Meta:
        model = Picture

    user = factory.SubFactory(UserFactory)
    picture_path = factory.Faker("picture_url")
    likes = UserFactory.create_batch(random.randint(0, 5))


class PictureCommentFactory(factory.Factory):
    class Meta:
        model = PictureComment

    user = factory.SubFactory(UserFactory)
    picture = factory.SubFactory(PictureFactory)
    text = factory.Faker("sentence")
    created_at = factory.LazyAttribute(datetime.datetime.now)


class CollectionFactory(factory.Factory):
    class Meta:
        model = Collection

    name = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    pictures = factory.RelatedFactoryList(
        PictureFactory, user=user, size=lambda: random.randint(0, 10)
    )


class ContestFactory(factory.Factory):
    class Meta:
        model = Contest

    title = factory.Faker("name")
    description = factory.Faker("sentence")
    cover_picture = factory.SubFactory(PictureFactory)
    prize = factory.Faker("sentence")
    automated_dates = factory.LazyAttribute(True)
    upload_phase_start = factory.LazyAttribute(datetime.datetime.now)
    upload_phase_end = factory.LazyAttribute(datetime.datetime.now)
    voting_phase_end = factory.LazyAttribute(datetime.datetime.now)
    active = factory.LazyAttribute(True)
    winners = factory.RelatedFactoryList(UserFactory, size=lambda: random.randint(0, 3))
    created_by = factory.LazyAttribute(cover_picture.user)


class ContestSubmissionFactory(factory.Factory):
    class Meta:
        model = ContestSubmission

    contest = factory.SubFactory(ContestFactory)
    picture = factory.SubFactory(PictureFactory)
    submissionDate = factory.LazyAttribute(datetime.datetime.now)
    votes = factory.RelatedFactoryList(UserFactory, size=lambda: random.randint(0, 10))
