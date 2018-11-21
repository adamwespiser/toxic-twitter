import logging
import sys
import time
from data_fetch_helpers import constants
from data_fetch_helpers.official_api_integration import api_integration as official_api
from data_fetch_helpers.scraper_integration import api_integration as scraper_api
from data_fetch_helpers.tweepy_integration import api_integration as tweepy_api

logger = logging.getLogger('toxicsense.data_fetch_helpers.public')

def get_tweets_of_user(username, limit=constants.DEFAULT_USER_TWEETS_LIMIT, data_source=constants.DATA_SOURCE_TWITTER_SCRAPER):
    result = []
    error = False
    try:
        logger.info('Tweets for user: ' + username + ' using ' + data_source)
        start = time.time()
        api = _get_api(data_source)
        result = api.get_user_tweets(username, limit=limit)
        end = time.time()
        logger.info('Took ' + str(end - start) + ' seconds')
    except:
        logger.exception(sys.exc_info())
        error = True
    return result, error


def get_tweets_from_search(search_term, limit=constants.DEFAULT_SEARCH_LIMIT, data_source=constants.DATA_SOURCE_TWITTER_SCRAPER):
    result = []
    error = False
    try:
        logger.info('Tweets for search: ' + search_term + ' using ' + data_source)
        start = time.time()
        api = _get_api(data_source)
        result = api.get_tweets_from_search(search_term, limit=limit)
        end = time.time()
        logger.info('Took ' + str(end - start) + ' seconds')
    except:
        logger.exception(sys.exc_info())
        error = True
    return result, error


def get_replies_of_tweet(tweet_id, username, limit=constants.DEFAULT_TWEET_REPLY_LIMIT, data_source=constants.DATA_SOURCE_TWITTER_SCRAPER):
    result = []
    error = False
    try:
        logger.info('Replies for tweet: ' + tweet_id + ' from user ' + username + ' using ' + data_source)
        start = time.time()
        api = _get_api(data_source)
        result = api.get_replies_of_tweet(tweet_id, username, limit=limit)
        end = time.time()
        logger.info('Took ' + str(end - start) + ' seconds')
    except:
        logger.exception(sys.exc_info())
        error = True
    return result, error


def _get_api(data_source):
    if data_source == constants.DATA_SOURCE_TWITTER_API:
        return official_api
    elif data_source == constants.DATA_SOURCE_TWEEPY:
        return tweepy_api
    else:
        return scraper_api
