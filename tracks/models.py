from django.db import models
from django.contrib.auth import get_user_model

# model for tracks
class Track(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    createdAt = models.DateTimeField(auto_now_add=True)
    postedBy = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


# model for likes for tracks
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    track = models.ForeignKey('tracks.Track', related_name='likes', on_delete=models.CASCADE)