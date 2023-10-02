from datetime import timedelta

import pytest
from django.test import TestCase
from django.utils import timezone

from photo.schema import schema
from photo.tests.factories import ContestFactory, PictureFactory, UserFactory
from .graphql_mutations import (
    contest_close_mutation,
    contest_creation_mutation,
    contest_update_mutation,
)


class ContestTest(TestCase):
    def setUp(self):
        self.user = UserFactory(user_profile_picture=True)
        self.picture = PictureFactory()

    @pytest.mark.asyncio
    async def test_create(self):
        contest = {
            "title": "Best contest",
            "description": "Epic pictures.",
            "prize": "Money.",
            "created_by": str(self.user.id),
            "cover_picture": self.picture.id,
        }

        result = await schema.execute(
            contest_creation_mutation,
            variable_values={"contest": contest},
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_contest"]["created_by"]["email"], self.user.email
        )
        self.assertEqual(
            result.data["create_contest"]["cover_picture"]["id"],
            self.picture.id,
        )
        self.assertEqual(result.data["create_contest"]["title"], contest["title"])
        self.assertEqual(
            result.data["create_contest"]["description"], contest["description"]
        )
        self.assertEqual(result.data["create_contest"]["prize"], contest["prize"])

    def test_close(self):
        contest = ContestFactory()

        result = schema.execute_sync(
            contest_close_mutation,
            variable_values={
                "contest": contest.id,
            },
        )

        self.assertEqual(result.errors, None)

    def test_update(self):
        user = UserFactory()
        contest = ContestFactory(created_by=user)
        picture = PictureFactory(user=user, file="www.test.com")

        updated_contest = {
            "id": contest.id,
            "title": "Title test",
            "description": "Description test",
            "cover_picture": picture.id,
            "prize": "Prize test",
            "upload_phase_end": str(timezone.now() + timedelta(1)),
            "voting_phase_end": str(timezone.now() + timedelta(2)),
        }

        result = schema.execute_sync(
            contest_update_mutation,
            variable_values={
                "contest": updated_contest,
            },
        )
        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_contest"]["title"], updated_contest["title"]
        )
        self.assertEqual(
            result.data["update_contest"]["description"], updated_contest["description"]
        )
        self.assertEqual(
            result.data["update_contest"]["prize"], updated_contest["prize"]
        )
        self.assertEqual(
            result.data["update_contest"]["cover_picture"]["id"],
            updated_contest["cover_picture"],
        )
        self.assertEqual(
            result.data["update_contest"]["upload_phase_end"],
            str(updated_contest["upload_phase_end"]).replace(" ", "T"),
        )
        self.assertEqual(
            result.data["update_contest"]["voting_phase_end"],
            str(updated_contest["voting_phase_end"]).replace(" ", "T"),
        )
