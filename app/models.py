from django.db import models

class Posts(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    score = models.IntegerField()
    url = models.URLField()
    posted_at = models.DateTimeField()  # Stores: 2025-12-05T04:00:28

