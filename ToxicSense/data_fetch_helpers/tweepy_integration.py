import tweepy
import urllib

from data_fetch_helpers import constants
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

    def get_replies_of_tweet(self, tweet_id, username, limit):
        status = self.api.get_status(tweet_id)
        results = []
        for reply in self._get_replies(status, username):
            results.append(reply)
            if (len(results) >= limit):
                break
        return tweet.Tweet.create_from_tweepy_response(results)

    def _get_replies(self, status, username):
        q = urllib.parse.urlencode({"q": "to:%s" % username})
        for reply in tweepy.Cursor(self.api.search, q=q, since_id=status.id).items(constants.DEFAULT_SEARCH_LIMIT):
            if reply.in_reply_to_status_id in (None, status.id):
                yield reply


api_integration = TweepyIntegration()