from django.utils import html

from toxicityanalyzer import toxicityanalyzer


class Tweet:
    
    @staticmethod
    def create_from_official_response(responses):
        tweets = []
        for response in responses:
            tweet = Tweet()
            tweet.user = response.user.screen_name
            tweet.timestamp = response.created_at
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

    def to_dict(self):
        return {
            'user': self.user,
            'timestamp': self.timestamp,
            'text': html.escape(self.text),
            'toxicity': toxicityanalyzer.get_toxicity(self.text)
        }
