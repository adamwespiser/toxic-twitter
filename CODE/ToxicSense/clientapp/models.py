from django.db import models

class Tweet(models.Model):
    tweet_id = models.IntegerField(unique=True)
    screen_name = models.CharField(max_length=16)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    toxicity = models.FloatField()


class Topic(models.Model):
    topic_term = models.CharField(max_length=150)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('topic_term', 'tweet')