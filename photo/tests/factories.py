from datetime import timedelta

import factory
import pytz
from django.core.files.base import ContentFile
from django.utils import timezone

from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from utils.enums import ContestInternalStates


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    user_handle = factory.Faker("name")
    email = factory.Sequence(lambda n: "user{0}@email.com".format(n))
    name_first = factory.Faker("first_name")
    name_last = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user{0}".format(n))
    password = factory.Sequence(lambda n: "user{0}password".format(n))
    created_at = factory.Faker("date_time", tzinfo=pytz.UTC)
    updated_at = factory.Faker("date_time", tzinfo=pytz.UTC)
    profile_picture_updated_at = timezone.now()

    @factory.post_generation
    def user_profile_picture(self, create, nullPicture=False):
        if not create or nullPicture:
            return

        self.profile_picture = PictureFactory(user=self)
        self.save()


class PictureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Picture
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("file_name")
    file = factory.LazyAttributeSequence(
        lambda _, n: ContentFile(
            factory.django.ImageField()._make_data(
                {"width": 1024, "height": 768, "color": "orange"}
            ),
            "picture{0}.jpg".format(n),
        )
    )

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
        skip_postgeneration_save = True

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
        skip_postgeneration_save = True

    title = factory.Faker("name")
    description = factory.Faker("sentence")
    created_by = factory.SubFactory(UserFactory, user_profile_picture=True)
    prize = factory.Faker("sentence")
    automated_dates = True
    upload_phase_start = timezone.now() - timedelta(days=3)
    upload_phase_end = None
    voting_phase_end = None
    internal_status = ContestInternalStates.OPEN

    @factory.post_generation
    def contest_auto_dates(self, create, auto_dates=True):
        if not create or not auto_dates:
            self.automated_dates = False
            return
        if not self.upload_phase_end:
            self.upload_phase_end = self.upload_phase_start + timedelta(days=15)
            if not self.voting_phase_end:
                self.voting_phase_end = self.upload_phase_end + timedelta(days=15)
        if self.voting_phase_end < timezone.now():
            self.internal_status = ContestInternalStates.CLOSED

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
        skip_postgeneration_save = True

    contest = factory.SubFactory(ContestFactory)
    picture = factory.SubFactory(
        PictureFactory, user=factory.SubFactory(UserFactory, user_profile_picture=True)
    )
    submission_date = timezone.now()

    @factory.post_generation
    def submission_votes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.votes.add(user)
            self.save()
