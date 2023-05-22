from django.test import TestCase

from photo.schema import schema
from tests.factories import CollectionFactory, PictureFactory, UserFactory


class PictureTest(TestCase):
    def setUp(self):
        self.batch = 10
        self.newPictures = PictureFactory.create_batch(
            self.batch, user=UserFactory(user_profile_picture=True)
        )
        self.newColletions = CollectionFactory.create_batch(
            self.batch, collection_pictures=self.newPictures
        )

    def test_query_all(self):
        query = """
                    query TestQuery {
                        collections {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), self.batch)
        self.assertEqual(len(result.data["collections"][0]["pictures"]), self.batch)

    def test_query_one(self):
        newPictures = PictureFactory.create_batch(
            3, user=UserFactory(user_profile_picture=True)
        )
        newColletion = CollectionFactory.create(collection_pictures=newPictures)

        query = """
                    query TestQuery($user_email: String!, $name: String!) {
                        collections(user_email: $user_email, name: $name) {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={
                "user_email": newColletion.user.email,
                "name": newColletion.name,
            },
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], newColletion.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["email"], newColletion.user.email
        )
        self.assertEqual(
            len(result.data["collections"][0]["pictures"]), len(newPictures)
        )

    def test_query_by_name(self):
        newPictures = PictureFactory.create_batch(
            3, user=UserFactory(user_profile_picture=True)
        )
        newColletion = CollectionFactory.create(collection_pictures=newPictures)

        query = """
                    query TestQuery($name: String!) {
                        collections(name: $name) {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"name": newColletion.name},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1)
        self.assertEqual(result.data["collections"][0]["name"], newColletion.name)
        self.assertEqual(
            result.data["collections"][0]["user"]["email"], newColletion.user.email
        )
        self.assertEqual(
            len(result.data["collections"][0]["pictures"]), len(newPictures)
        )

    def test_query_by_user(self):
        newPictures = PictureFactory.create_batch(
            3, user=UserFactory(user_profile_picture=True)
        )
        newColletion = CollectionFactory.create(collection_pictures=newPictures)
        otherCollections = CollectionFactory.create_batch(3, user=newColletion.user)

        query = """
                    query TestQuery($user_email: String!) {
                        collections(user_email: $user_email) {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
                            }
                        }
                    }
                """

        result = schema.execute_sync(
            query,
            variable_values={"user_email": newColletion.user.email},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(len(result.data["collections"]), 1 + len(otherCollections))
        for collection in result.data["collections"]:
            self.assertEqual(collection["user"]["email"], newColletion.user.email)
