from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from photo.models import Contest
from photo.schema import schema
from photo.tests.factories import ContestFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    contest_query_all,
    contest_query_creator,
    contest_query_one,
    contest_query_search,
)


class ContestTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.contests = ContestFactory.create_batch(self.batch)

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
        contest = ContestFactory.create()

        query = contest_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": contest.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 1)
        self.assertEqual(result.data["contests"][0]["id"], contest.id)

    def test_query_by_creator(self):
        user = UserFactory()
        contests = ContestFactory.create_batch(3, created_by=user)

        query = contest_query_creator

        result = schema.execute_sync(
            query,
            variable_values={"user": str(user.id)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), len(contests))
        self.assertEqual(result.data["contests"][0]["created_by"]["id"], str(user.id))

    def test_query_status(self):
        user = UserFactory()
        currentTime = timezone.now()

        contest_schedule = ContestFactory(
            created_by=user,
            upload_phase_start=currentTime + timedelta(days=1),
            upload_phase_end=currentTime + timedelta(days=2),
            voting_phase_end=currentTime + timedelta(days=3),
        )
        contest_open = ContestFactory(
            created_by=user,
            upload_phase_start=currentTime - timedelta(days=1),
            upload_phase_end=currentTime + timedelta(days=1),
            voting_phase_end=currentTime + timedelta(days=2),
        )
        contest_voting = ContestFactory(
            created_by=user,
            upload_phase_start=currentTime - timedelta(days=3),
            upload_phase_end=currentTime - timedelta(days=2),
            voting_phase_end=currentTime + timedelta(days=1),
        )
        contest_close = ContestFactory(
            created_by=user,
            upload_phase_start=currentTime - timedelta(days=3),
            upload_phase_end=currentTime - timedelta(days=2),
            voting_phase_end=currentTime - timedelta(days=1),
        )
        status = {
            str(contest_schedule.id): "scheduled",
            str(contest_open.id): "open",
            str(contest_voting.id): "voting",
            str(contest_close.id): "closed",
        }

        query = contest_query_creator

        result = schema.execute_sync(
            query,
            variable_values={"user": str(user.id)},
        )

        self.assertEqual(result.errors, None)
        for contest in result.data["contests"]:
            self.assertEqual(contest["status"], status[str(contest["id"])])

    def test_query_search(self):
        testText = "This is a text with a weird word 1234Test1234."

        contest_title = ContestFactory(title=testText)
        contest_description = ContestFactory(description=testText)
        contest_prize = ContestFactory(prize=testText)

        contest_IDs = [
            contest.id
            for contest in [contest_title, contest_description, contest_prize]
        ]

        query = contest_query_search

        result = schema.execute_sync(
            query,
            variable_values={"search": "1234Test1234"},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contest_search"]), 3)
        for contest in result.data["contest_search"]:
            self.assertTrue(contest["id"] in contest_IDs)
