import random

import django.db.models.signals as signals
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
    profile_picture_updated_at = factory.Faker("date_time", tzinfo=pytz.UTC)

    @factory.post_generation
    def user_profile_picture(self, create, nullPicture=False):
        if not create or nullPicture:
            return

        self.profile_picture = PictureFactory(user=self)
        self.save()


@factory.django.mute_signals(signals.post_save)
class PictureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Picture

    user = factory.SubFactory(UserFactory)
    picture_path = factory.Faker("url")

    @factory.post_generation
    def user_likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.likes.add(user)
            self.save()


class PictureCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PictureComment

    user = factory.SubFactory(UserFactory, user_profile_picture=True)
    picture = factory.SubFactory(
        PictureFactory, user=factory.SubFactory(UserFactory, user_profile_picture=True)
    )
    text = factory.Faker("sentence")
    created_at = factory.Faker("date_time", tzinfo=pytz.UTC)


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    name = factory.Faker("name")
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def collection_pictures(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for picture in extracted:
                self.pictures.add(picture)
            self.save()


class ContestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contest

    title = factory.Faker("name")
    description = factory.Faker("sentence")
    created_by = factory.SubFactory(UserFactory, user_profile_picture=True)
    prize = factory.Faker("sentence")
    automated_dates = True
    upload_phase_start = factory.Faker("date_time", tzinfo=pytz.UTC)
    upload_phase_end = factory.Faker("date_time", tzinfo=pytz.UTC)
    voting_phase_end = factory.Faker("date_time", tzinfo=pytz.UTC)
    active = True

    @factory.post_generation
    def contest_cover_picture(self, create, nullPicture=False):
        if not create or nullPicture:
            return

        self.cover_picture = PictureFactory(user=self.created_by)
        self.save()

    @factory.post_generation
    def contest_winners(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.winners.add(user)
            self.save()


class ContestSubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContestSubmission

    contest = factory.SubFactory(ContestFactory)
    picture = factory.SubFactory(PictureFactory)
    submissionDate = factory.Faker("date_time", tzinfo=pytz.UTC)
    votes = factory.RelatedFactoryList(UserFactory, size=lambda: random.randint(0, 10))
