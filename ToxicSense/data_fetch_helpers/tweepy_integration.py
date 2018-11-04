import tweepy

from data_fetch_helpers import creds
from data_fetch_helpers import tweet
from data_fetch_helpers.api_integration_base import ApiIntegration

class TweepyIntegration(ApiIntegration):

    def __init__(self):
        # AppAuthenticated API allows 450 requests per 15 minutes (limited to few APIs)
        app_auth = tweepy.AppAuthHandler(creds.TWITTER_OFFICIAL_CONSUMER_KEY, creds.TWITTER_OFFICIAL_CONSUMER_SECRET)
        self.api = tweepy.API(app_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # UserAuthenticated API allows 180 requests per 15 minutes
        user_auth = tweepy.OAuthHandler(creds.TWITTER_OFFICIAL_CONSUMER_KEY, creds.TWITTER_OFFICIAL_CONSUMER_KEY)
        user_auth.set_access_token(creds.TWITTER_OFFICIAL_ACCESS_TOKEN, creds.TWITTER_OFFICIAL_ACCESS_TOKEN_SECRET)
        self.user_api = tweepy.API(user_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    def get_user_tweets(self, username, limit):
        tweets = tweepy.Cursor(self.api.user_timeline, screen_name=username).items(limit)
        return tweet.Tweet.create_from_tweepy_response(tweets)
    
    def get_tweets_from_search(self, search_term, limit):
        
        tweets = tweepy.Cursor(self.api.search, q=search_term, lang='en').items(limit)
        return tweet.Tweet.create_from_tweepy_response(tweets)


api_integration = TweepyIntegration()