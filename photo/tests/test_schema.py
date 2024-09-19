import pytest
from photo.models import Picture

@pytest.mark.django_db
def test_picture_creation():
    picture = Picture.objects.create(
        user_id=1,
        file='test.jpg',
        description='Test Description'
    )
    assert picture.id is not None
    assert picture.description == 'Test Description'