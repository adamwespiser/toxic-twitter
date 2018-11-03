from data_fetch_helpers import constants
from data_fetch_helpers.official_api_integration import api_integration as official_api
from data_fetch_helpers.scraper_integration import api_integration as scraper_api


def get_tweets_of_user(
    username, limit=constants.DEFAULT_USER_TWEETS_LIMIT,
    data_source=constants.DATA_SOURCE_TWITTER_SCRAPER
):
    print('Tweets for user: ', username, 'using', data_source)
    api = _get_api(data_source)
    return api.get_user_tweets(username, limit=limit)


def get_tweets_from_search(
    search_term, limit=constants.DEFAULT_SEARCH_LIMIT,
    data_source=constants.DATA_SOURCE_TWITTER_SCRAPER
):
    print('Tweets for search: ', search_term, 'using', data_source)
    api = _get_api(data_source)
    return api.get_tweets_from_search(search_term, limit=limit)


def _get_api(data_source):
    if data_source == constants.DATA_SOURCE_TWITTER_API:
        return official_api
    else:
        return scraper_api
