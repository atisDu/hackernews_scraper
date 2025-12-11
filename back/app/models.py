from django.db import models

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    score = models.IntegerField()
    url = models.URLField(max_length=1024) #Django defaultā ir tikai 200, kas radīja errorus glabājot dažus postus db
    posted_at = models.DateTimeField()  # Glabā: 2025-12-05T04:00:28
    def __str__(self):
        return self.title

