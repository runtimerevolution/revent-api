from django.test import TestCase

from photo.models import PictureComment
from photo.schema import schema
from photo.tests.factories import PictureCommentFactory, PictureFactory
from photo.tests.test_queries.graphql_queries import (
    picture_comment_query_all,
    picture_comment_query_filters,
)


class PictureCommentTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.new_pictures = PictureCommentFactory.create_batch(self.batch)

    def test_query_all(self):
        result = schema.execute_sync(
            picture_comment_query_all,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["picture_comments"][0].keys()]),
            sorted([field.name for field in PictureComment._meta.fields]),
        )

    def test_query_filters_id(self):
        picture_comment = PictureCommentFactory.create()

        result = schema.execute_sync(
            picture_comment_query_filters,
            variable_values={"filters": {"id": picture_comment.id}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), 1)
        self.assertEqual(result.data["picture_comments"][0]["id"], picture_comment.id)
        self.assertEqual(
            result.data["picture_comments"][0]["text"], picture_comment.text
        )

    def test_query_filters_picture(self):
        picture = PictureFactory()
        picture_comments = PictureCommentFactory.create_batch(3, picture=picture)

        result = schema.execute_sync(
            picture_comment_query_filters,
            variable_values={"filters": {"picture": {"id": picture.id}}},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["picture"]["id"],
            picture.id,
        )
        self.assertEqual(len(result.data["picture_comments"]), len(picture_comments))
