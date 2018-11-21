import logging
import twitter
import urllib.parse

from data_fetch_helpers import creds
from data_fetch_helpers import tweet
from data_fetch_helpers.api_integration_base import ApiIntegration


class OfficialApiIntegration(ApiIntegration):

    def __init__(self):
        self.api = twitter.Api(
            consumer_key=creds.TWITTER_OFFICIAL_CONSUMER_KEY,
            consumer_secret=creds.TWITTER_OFFICIAL_CONSUMER_SECRET,
            access_token_key=creds.TWITTER_OFFICIAL_ACCESS_TOKEN,
            access_token_secret=creds.TWITTER_OFFICIAL_ACCESS_TOKEN_SECRET
        )
    
    def get_user_tweets(self, username, limit):
        results = self.api.GetUserTimeline(screen_name=username, count=limit)
        return tweet.Tweet.create_from_official_response(results)
    
    def get_tweets_from_search(self, search_term, limit):
        results = self.api.GetSearch(term=search_term, count=limit)
        return tweet.Tweet.create_from_official_response(results)

    def get_replies_of_tweet(self, tweet_id, username, limit):
        results = []
        for reply in self._get_replies(tweet_id, username):
            results.append(reply)
            if (len(results) >= limit):
                break
        return tweet.Tweet.create_from_official_response(results)

    def _get_replies(self, tweet_id, username):
        max_id = None
        while True:
            q = urllib.parse.urlencode({"q": "to:%s" % username})
            q += '&count=100&since_id=' + tweet_id
            if max_id is not None:
                q += '&max_id=' + str(max_id)
            try:
                replies = self.api.GetSearch(raw_query=q)
                if (len(replies) == 0):
                    break
            except twitter.error.TwitterError as e:
                logging.error("caught twitter api error: %s", e)
                break
            for reply in replies:
                if reply.in_reply_to_status_id in (None, tweet_id):
                    yield reply
                    max_id = reply.id


api_integration = OfficialApiIntegration()
