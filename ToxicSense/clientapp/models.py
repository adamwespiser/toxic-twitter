from django.db import models

class Topic(models.Model):
    topic_term = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.topic_term


class Tweet(models.Model):
    tweet_id = models.IntegerField(unique=False)
    screen_name = models.CharField(max_length=16)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    toxicity = models.FloatField()
    topics = models.ManyToManyField(Topic, related_name='tweets')