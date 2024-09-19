
from typing import List

import strawberry
from strawberry.file_uploads import Upload
from strawberry_django_plus import gql
from .models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)

@strawberry.django.input(Picture)
class PictureInput:
    user: str
    file: Upload
    description: str

@gql.django.partial(Picture)
class PictureInputPartial:
    id: int
    likes: List[str]