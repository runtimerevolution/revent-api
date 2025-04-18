
from typing import List

import strawberry
from strawberry_django_plus import gql
from .models import Picture

@strawberry.type
class PictureType:
    id: strawberry.ID
    user: UserType
    file: str
    description: str
    likes: List[UserType]

@gql.django.input(Picture)
class PictureInput:
    user: strawberry.ID
    file: strawberry.String
    description: strawberry.String

@gql.django.partial(Picture)
class PictureInputPartial:
    id: strawberry.ID
    likes: List[str]