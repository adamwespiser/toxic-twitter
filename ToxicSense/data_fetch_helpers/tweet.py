import time
from datetime import datetime

from django.utils import html

from toxicityanalyzer import toxicityanalyzer


class Tweet:
    
    @staticmethod
    def create_from_official_response(responses):
        tweets = []
        TWITTER_DATETIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
        OUR_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
        for response in responses:
            tweet = Tweet()
            tweet.user = response.user.screen_name
            tweet.timestamp = time.strftime(
                OUR_DATETIME_FORMAT,
                time.strptime(
                    response.created_at,
                    TWITTER_DATETIME_FORMAT
                )
            )
            tweet.text = response.text
            tweets.append(tweet)
        return tweets

    @staticmethod
    def create_from_scraper_response(responses):
        tweets = []
        for response in responses:
            tweet = Tweet()
            tweet.user = response.user
            tweet.timestamp = response.timestamp
            tweet.text = response.text
            tweets.append(tweet)
        return tweets

    @staticmethod
    def create_from_tweepy_response(responses):
        tweets = []
        OUR_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
        for response in responses:
            tweet = Tweet()
            tweet.user = response.user.screen_name
            tweet.timestamp = response.created_at.strftime(OUR_DATETIME_FORMAT)
            tweet.text = response.text
            tweets.append(tweet)
        return tweets

    def to_dict(self):
        return {
            'user': self.user,
            'timestamp': self.timestamp,
            'text': html.escape(self.text),
            'toxicity': toxicityanalyzer.get_toxicity(self.text)
        }
