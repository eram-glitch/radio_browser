
from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField()
    country = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'station_id')

    def __str__(self):
        return f"{self.user.username} - {self.name}"
