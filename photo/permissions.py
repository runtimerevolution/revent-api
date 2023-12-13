from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User not authenticated."

    def has_permission(self, source: any, info: Info, **kwargs) -> bool:
        if not info.context.user():
            return False
        return True
