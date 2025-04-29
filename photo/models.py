
from django.db import models

class Picture(SoftDeleteModel):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="picture_user"
    )
    name = models.TextField(blank=True, null=True)
    file = models.ImageField(
        storage=PublicMediaStorage(),
        upload_to=picture_path,
    )
    likes = models.ManyToManyField(User, related_name="picture_likes", blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def like_picture(self, user):
        if user not in self.likes.filter(id=user):
            self.likes.add(user)
            self.save()
        return self


class PictureComment(SoftDeleteModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)