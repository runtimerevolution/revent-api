
from django.db import models

class Picture(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='pictures/')
    likes = models.ManyToManyField('users.User', related_name='liked_pictures')
    description = models.TextField(blank=True, null=True)