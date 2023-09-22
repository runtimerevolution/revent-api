from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from tests.factories import ContestFactory, UserFactory
from tests.test_queries.query_file import (
    contest_query_all,
    contest_query_creator,
    contest_query_one,
    contest_query_search,
)

from photo.models import Contest
from photo.schema import schema


class ContestTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newContests = ContestFactory.create_batch(self.batch)

    def test_query_all(self):
        query = contest_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["contests"][0].keys()]),
            sorted(
                [
                    field.name
                    for field in (Contest._meta.fields + Contest._meta.many_to_many)
                ]
                + ["status"]
            ),
        )

    def test_query_one(self):
        newContest = ContestFactory.create()

        query = contest_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": newContest.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 1)
        self.assertEqual(result.data["contests"][0]["id"], newContest.id)

    def test_query_by_creator(self):
        newUser = UserFactory()
        newContests = ContestFactory.create_batch(3, created_by=newUser)

        query = contest_query_creator

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), len(newContests))
        self.assertEqual(
            result.data["contests"][0]["created_by"]["email"], newUser.email
        )

    def test_query_status(self):
        newUser = UserFactory()
        currentTime = timezone.now()

        newContestSchedule = ContestFactory(
            created_by=newUser,
            upload_phase_start=currentTime + timedelta(days=1),
            upload_phase_end=currentTime + timedelta(days=2),
            voting_phase_end=currentTime + timedelta(days=3),
        )
        newContestOpen = ContestFactory(
            created_by=newUser,
            upload_phase_start=currentTime - timedelta(days=1),
            upload_phase_end=currentTime + timedelta(days=1),
            voting_phase_end=currentTime + timedelta(days=2),
        )
        newContestVoting = ContestFactory(
            created_by=newUser,
            upload_phase_start=currentTime - timedelta(days=3),
            upload_phase_end=currentTime - timedelta(days=2),
            voting_phase_end=currentTime + timedelta(days=1),
        )
        newContestClose = ContestFactory(
            created_by=newUser,
            upload_phase_start=currentTime - timedelta(days=3),
            upload_phase_end=currentTime - timedelta(days=2),
            voting_phase_end=currentTime - timedelta(days=1),
        )
        status = {
            str(newContestSchedule.id): "scheduled",
            str(newContestOpen.id): "open",
            str(newContestVoting.id): "voting",
            str(newContestClose.id): "closed",
        }

        query = contest_query_creator

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        for contest in result.data["contests"]:
            self.assertEqual(contest["status"], status[str(contest["id"])])

    def test_query_search(self):

        testText = "This is a text with a weird word 1234Test1234."

        newContestTitle = ContestFactory(title=testText)
        newContestDescription = ContestFactory(description=testText)
        newContestPrize = ContestFactory(prize=testText)

        newContestIDs = [
            contest.id
            for contest in [newContestTitle, newContestDescription, newContestPrize]
        ]

        query = contest_query_search

        result = schema.execute_sync(
            query,
            variable_values={"search": "1234Test1234"},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_search"]), 3)
        for contest in result.data["contest_search"]:
            self.assertTrue(contest["id"] in newContestIDs)
