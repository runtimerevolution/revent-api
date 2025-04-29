from django.test import TestCase
from .models import Picture, User

class PictureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email='testuser@example.com')
        Picture.objects.create(
            user=test_user,
            name='Test Picture',
            description='Test Description',
        )

    def test_description_content(self):
        picture = Picture.objects.get(id=1)
        expected_object_name = f'{picture.description}'
        self.assertEqual(expected_object_name, 'Test Description')