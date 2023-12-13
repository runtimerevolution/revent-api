from django.db import models


class ContestInternalStates(models.TextChoices):
    OPEN = "open"
    CLOSED = "closed"
    DRAW = "draw"
