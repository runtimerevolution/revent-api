import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.forms import ValidationError
from PIL import Image
from io import BytesIO

from photo.mutations import picture_creation
from photo.models import User, Picture
from photo.inputs import PictureInput
from photo.fixtures import NO_USER_FOUND, PICTURE_SIZE_ERROR, CREATE_PICTURE_ERROR

@pytest.fixture
def test_user():
    return User.objects.create(id="test_user")

@pytest.fixture
def test_image():
    image = Image.new('RGB', (100, 100), color='red')
    image_bytes = BytesIO()
    image.save(image_bytes, format='webp')
    image_bytes.seek(0)
    return image_bytes

def test_picture_creation_success(test_user, test_image):
    # Create test input
    file = SimpleUploadedFile("test.webp", test_image.getvalue(), content_type="image/webp")
    input = PictureInput(user=test_user.id, file=file)

    # Test picture creation
    response = picture_creation(input=input)

    assert response.success is True
    assert response.errors == ""
    assert isinstance(response.results, Picture)
    assert response.results.user == test_user
    assert response.results.name == str(response.results.id)

def test_picture_creation_invalid_user():
    # Create test input with non-existent user
    file = SimpleUploadedFile("test.webp", b"test", content_type="image/webp")
    input = PictureInput(user="non_existent_user", file=file)

    # Test picture creation
    response = picture_creation(input=input)

    assert response.success is False
    assert response.errors == NO_USER_FOUND
    assert response.results == {}

def test_picture_creation_large_file(test_user, settings):
    # Create a large test file
    large_image = Image.new('RGB', (1000, 1000), color='red')
    image_bytes = BytesIO()
    large_image.save(image_bytes, format='webp')
    image_bytes.seek(0)

    # Set a small max file size for testing
    settings.MAX_PICTURE_SIZE = 100

    file = SimpleUploadedFile("test.webp", image_bytes.getvalue(), content_type="image/webp")
    input = PictureInput(user=test_user.id, file=file)

    # Test picture creation
    response = picture_creation(input=input)

    assert response.success is False
    assert response.errors == PICTURE_SIZE_ERROR
    assert response.results == {}
