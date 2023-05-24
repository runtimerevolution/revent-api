from django.test import TestCase

from photo.schema import schema
from tests.factories import PictureCommentFactory, PictureFactory, UserFactory
from tests.test_queries.query_file import (
    picture_comment_query_all,
    picture_comment_query_one,
    picture_comment_query_picture,
    picture_comment_query_user,
)


class PictureCommentTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newPictures = PictureCommentFactory.create_batch(self.batch)

    def test_query_all(self):
        query = picture_comment_query_all

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), self.batch)

    def test_query_one(self):
        newPictureComment = PictureCommentFactory.create()

        query = picture_comment_query_one

        result = schema.execute_sync(
            query,
            variable_values={"id": newPictureComment.id},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["picture_comments"]), 1)
        self.assertEqual(result.data["picture_comments"][0]["id"], newPictureComment.id)
        self.assertEqual(
            result.data["picture_comments"][0]["text"], newPictureComment.text
        )

    def test_query_by_user(self):
        newUser = UserFactory()
        newPictureComments = PictureCommentFactory.create_batch(3, user=newUser)

        query = picture_comment_query_user

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newUser.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["user"]["email"], newUser.email
        )
        self.assertEqual(len(result.data["picture_comments"]), len(newPictureComments))

    def test_query_by_picture(self):
        newPicture = PictureFactory()
        newPictureComments = PictureCommentFactory.create_batch(3, picture=newPicture)

        query = picture_comment_query_picture

        result = schema.execute_sync(
            query,
            variable_values={"picture_path": newPicture.picture_path},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(
            result.data["picture_comments"][0]["picture"]["picture_path"],
            newPicture.picture_path,
        )
        self.assertEqual(len(result.data["picture_comments"]), len(newPictureComments))
