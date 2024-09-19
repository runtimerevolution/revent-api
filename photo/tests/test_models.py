from django.test import TestCase
from photo.models import Picture

class PictureModelTestCase(TestCase):
    def test_picture_description_field(self):
        picture = Picture.objects.create(
            user_id=1,
            file='test.jpg',
            description='Test Description'
        )
        self.assertEqual(picture.description, 'Test Description')
        self.assertEqual(picture.description, 'Test Description')

    def test_new_field_description(self):
        picture = Picture.objects.create(
            user_id=1,
            file='test.jpg',
            description='Test Description'
        )
        self.assertEqual(picture.description, 'Test Description')

        picture.description = 'Updated Description'
        picture.save()
        self.assertEqual(picture.description, 'Updated Description')