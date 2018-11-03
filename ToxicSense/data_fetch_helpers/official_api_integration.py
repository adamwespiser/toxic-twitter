import twitter

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


api_integration = OfficialApiIntegration()
