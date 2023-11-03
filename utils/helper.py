from django.contrib.auth.backends import ModelBackend

from photo.models import User


class ReventModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
