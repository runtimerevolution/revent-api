from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from photo.models import Contest
from photo.schema import schema
from photo.tests.factories import ContestFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    contest_query_all,
    contest_query_filters,
    contest_query_search,
    contest_query_status,
    contest_query_time,
)


class ContestTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.contests = ContestFactory.create_batch(self.batch)

    def test_query_all(self):
        result = schema.execute_sync(
            contest_query_all,
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

        result = schema.execute_sync(
            contest_query_filters,
            variable_values={"filters": {"id": contest.id}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 1)
        self.assertEqual(result.data["contests"][0]["id"], contest.id)

    def test_query_by_creator(self):
        user = UserFactory()
        contests = ContestFactory.create_batch(3, created_by=user)

        result = schema.execute_sync(
            contest_query_filters,
            variable_values={"filters": {"created_by": {"id": str(user.id)}}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), len(contests))
        self.assertEqual(result.data["contests"][0]["created_by"]["id"], str(user.id))

    def test_query_status(self):
        user = UserFactory()
        time = timezone.now()

        contest_schedule = ContestFactory(
            created_by=user,
            upload_phase_start=time + timedelta(days=1),
            upload_phase_end=time + timedelta(days=2),
            voting_phase_end=time + timedelta(days=3),
        )
        contest_open = ContestFactory(
            created_by=user,
            upload_phase_start=time - timedelta(days=1),
            upload_phase_end=time + timedelta(days=1),
            voting_phase_end=time + timedelta(days=2),
        )
        contest_voting = ContestFactory(
            created_by=user,
            upload_phase_start=time - timedelta(days=3),
            upload_phase_end=time - timedelta(days=2),
            voting_phase_end=time + timedelta(days=1),
        )
        contest_close = ContestFactory(
            created_by=user,
            upload_phase_start=time - timedelta(days=3),
            upload_phase_end=time - timedelta(days=2),
            voting_phase_end=time - timedelta(days=1),
        )
        status = {
            str(contest_schedule.id): "scheduled",
            str(contest_open.id): "open",
            str(contest_voting.id): "voting",
            str(contest_close.id): "closed",
        }

        result = schema.execute_sync(
            contest_query_filters,
            variable_values={"filters": {"created_by": {"id": str(user.id)}}},
        )

        self.assertEqual(result.errors, None)
        for contest in result.data["contests"]:
            self.assertEqual(contest["status"], status[str(contest["id"])])


class ContestFilterTest(TestCase):
    def test_query_filter_search(self):
        test_text = "This is a text with a weird word 1234Test1234."

        contest_title = ContestFactory(
            title=test_text, description="sample", prize="sample"
        )
        contest_description = ContestFactory(
            title="sample", description=test_text, prize="sample"
        )
        contest_prize = ContestFactory(
            title="sample", description="sample", prize=test_text
        )

        contest_IDs = [
            contest.id
            for contest in [contest_title, contest_description, contest_prize]
        ]

        result = schema.execute_sync(
            contest_query_search,
            variable_values={"filters": {"search": "test"}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 3)
        for contest in result.data["contests"]:
            self.assertTrue(contest["id"] in contest_IDs)

    def test_query_filter_time(self):
        time = timezone.now().replace(year=2020, month=4)

        ContestFactory(
            upload_phase_start=time,
        )

        ContestFactory(
            upload_phase_start=time + timedelta(days=31),
        )

        ContestFactory(
            upload_phase_start=time + timedelta(days=366),
        )

        result_month = schema.execute_sync(
            contest_query_time,
            variable_values={
                "filters": {
                    "upload_phase_start": {
                        "range": (
                            str(time.replace(day=1, hour=0, minute=0, second=0)),
                            str(time.replace(day=30, hour=23, minute=59, second=59)),
                        )
                    }
                }
            },
        )

        result_year = schema.execute_sync(
            contest_query_time,
            variable_values={
                "filters": {
                    "upload_phase_start": {
                        "range": (
                            str(
                                time.replace(month=1, day=1, hour=0, minute=0, second=0)
                            ),
                            str(
                                time.replace(
                                    month=12, day=31, hour=23, minute=59, second=59
                                )
                            ),
                        )
                    }
                }
            },
        )

        self.assertEqual(result_month.errors, None)
        self.assertEqual(result_year.errors, None)
        self.assertEqual(len(result_month.data["contests"]), 1)
        self.assertEqual(len(result_year.data["contests"]), 2)

    def test_query_filter_status(self):
        time = timezone.now()

        contest_voting = ContestFactory(
            upload_phase_start=time - timedelta(days=3),
            upload_phase_end=time - timedelta(days=2),
            voting_phase_end=time + timedelta(days=1),
        )

        result = schema.execute_sync(
            contest_query_status,
            variable_values={"filters": {"status": "voting"}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["contests"]), 1)
        self.assertEqual(result.data["contests"][0]["id"], contest_voting.id)
        self.assertEqual(result.data["contests"][0]["status"], "voting")
