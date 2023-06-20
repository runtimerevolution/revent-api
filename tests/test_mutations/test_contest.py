from datetime import timedelta

import pytest
from django.test import TestCase
from django.utils import timezone

from photo.schema import schema
from tests.factories import ContestFactory, PictureFactory, UserFactory
from tests.test_mutations.mutation_file import (
    contest_close_mutation,
    contest_creation_mutation,
    contest_update_mutation,
)
from tests.test_queries.query_file import picture_query_one, user_query_one


class ContestTest(TestCase):
    def setUp(self):
        newUser = UserFactory(user_profile_picture=True)
        newPicture = PictureFactory()

        newUserResult = schema.execute_sync(
            user_query_one,
            variable_values={"email": newUser.email},
        )
        newPictureResult = schema.execute_sync(
            picture_query_one,
            variable_values={"picture_path": newPicture.picture_path},
        )

        self.newUser = newUserResult.data["users"][0]
        self.newPicture = newPictureResult.data["pictures"][0]

    @pytest.mark.asyncio
    async def test_create_one(self):
        mutation = contest_creation_mutation
        newUser = self.newUser
        newPicture = self.newPicture

        newContest = {
            "title": "Best contest",
            "description": "Epic pictures.",
            "prize": "Money.",
            "active": True,
            "created_by": newUser["email"],
            "cover_picture": newPicture["picture_path"],
        }

        result = await schema.execute(
            mutation,
            variable_values={"contest": newContest},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["create_contest"]["created_by"]["email"], newUser["email"]
        )
        self.assertEqual(
            result.data["create_contest"]["cover_picture"]["picture_path"],
            newPicture["picture_path"],
        )
        self.assertEqual(result.data["create_contest"]["title"], newContest["title"])
        self.assertEqual(
            result.data["create_contest"]["description"], newContest["description"]
        )
        self.assertEqual(result.data["create_contest"]["prize"], newContest["prize"])
        self.assertEqual(result.data["create_contest"]["active"], newContest["active"])

    def test_close(self):
        mutation = contest_close_mutation

        newContest = ContestFactory()

        result = schema.execute_sync(
            mutation,
            variable_values={
                "contest": newContest.id,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["contest_close"]["active"],
            False,
        )

    def test_update(self):
        mutation = contest_update_mutation

        newUser = UserFactory()
        newContest = ContestFactory(created_by=newUser)
        newPicture = PictureFactory(user=newUser, picture_path="www.test.com")

        updatedContest = {
            "id": newContest.id,
            "title": "Title test",
            "description": "Description test",
            "cover_picture": newPicture.picture_path,
            "prize": "Prize test",
            "upload_phase_end": str(timezone.now() + timedelta(1)),
            "voting_phase_end": str(timezone.now() + timedelta(2)),
        }

        result = schema.execute_sync(
            mutation,
            variable_values={
                "contest": updatedContest,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["update_contest"]["title"], updatedContest["title"]
        )
        self.assertEqual(
            result.data["update_contest"]["description"], updatedContest["description"]
        )
        self.assertEqual(
            result.data["update_contest"]["prize"], updatedContest["prize"]
        )
        self.assertEqual(
            result.data["update_contest"]["cover_picture"]["picture_path"],
            updatedContest["cover_picture"],
        )
        self.assertEqual(
            result.data["update_contest"]["upload_phase_end"],
            str(updatedContest["upload_phase_end"]).replace(" ", "T"),
        )
        self.assertEqual(
            result.data["update_contest"]["voting_phase_end"],
            str(updatedContest["voting_phase_end"]).replace(" ", "T"),
        )
