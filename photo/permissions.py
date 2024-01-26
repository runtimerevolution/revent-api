import hashlib

from django.conf import settings
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User not authenticated."

    def has_permission(self, source: any, info: Info, **kwargs) -> bool:
        if (
            isinstance(info.context, dict)
            and info.context["test"]
            and info.context["authentication"]
        ):
            hashed_password = hashlib.sha256((settings.SECRET_KEY).encode("UTF-8"))
            return (
                info.context["authentication"].hexdigest()
                == hashed_password.hexdigest()
            )
        if not info.context.user():
            return False
        return True
