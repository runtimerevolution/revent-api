from django.test import TestCase

from photo.models import PictureComment
from photo.schema import schema
from photo.tests.factories import PictureCommentFactory, PictureFactory, UserFactory
from photo.tests.test_queries.graphql_queries import (
    picture_comment_query_all,
    picture_comment_query_one,
    picture_comment_query_picture,
    picture_comment_query_user,
)


class PictureCommentTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.new_pictures = PictureCommentFactory.create_batch(self.batch)

    def test_query_all(self):
        query = picture_comment_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), self.batch)
        self.assertEqual(
            sorted([key for key in result.data["picture_comments"][0].keys()]),
            sorted([field.name for field in PictureComment._meta.fields]),
        )

    def test_query_one(self):
        picture_comment = PictureCommentFactory.create()

        query = picture_comment_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": picture_comment.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), 1)
        self.assertEqual(result.data["picture_comments"][0]["id"], picture_comment.id)
        self.assertEqual(
            result.data["picture_comments"][0]["text"], picture_comment.text
        )

    def test_query_by_user(self):
        user = UserFactory()
        picture_comments = PictureCommentFactory.create_batch(3, user=user)

        query = picture_comment_query_user

        result = schema.execute_sync(
            query,
            variable_values={"user": str(user.id)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["user"]["email"], user.email
        )
        self.assertEqual(len(result.data["picture_comments"]), len(picture_comments))

    def test_query_by_picture(self):
        picture = PictureFactory()
        picture_comments = PictureCommentFactory.create_batch(3, picture=picture)

        query = picture_comment_query_picture

        result = schema.execute_sync(
            query,
            variable_values={"picture_id": picture.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["picture"]["id"],
            picture.id,
        )
        self.assertEqual(len(result.data["picture_comments"]), len(picture_comments))
