import json

from clientapp import constants
from clientapp import summarizer
from clientapp import utils
from data_fetch_helpers import constants as data_fetch_constants
from data_fetch_helpers import public as data_fetch_public


TOXICITY_THRESHOLD = constants.TOXICITY_THRESHOLD
MAX_DEPTH = 2

def get_graph_for_topic(topic, limit=50):
    # print('Loading topic results')
    tweets, error = data_fetch_public.get_tweets_from_search(
        topic, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    if error:
        return []
    return get_graph_for_tweets(tweets, limit)


def get_graph_for_tweet(user, tweet_id, limit=50):
    tweets, error = data_fetch_public.get_replies_of_tweet(
        tweet_id, user, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    if error:
        return []
    return get_graph_for_tweets(tweets, limit)


def get_graph_for_user(user, limit=50):
    tweets, error = data_fetch_public.get_tweets_of_user(
        user, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    if error:
        return []
    summary = summarizer.get_results_summary(tweets, TOXICITY_THRESHOLD)
    # print('Top mentions:', summary.top_mentioned_users)
    all_tweets = tweets
    all_tweets.extend(
        _get_tweets_from_user_scores(summary.top_mentioned_users.items(), limit)
    )
    # print('Top hashtags:', summary.top_hashtags)
    all_tweets.extend(
        _get_tweets_from_hashtag_scores(summary.top_hashtags.items(), limit)
    )
    return [data_point for data_point in yield_data_points_from_tweets(all_tweets)]


def get_graph_for_tweets(tweets, limit, should_go_deep=True):
    all_tweets = tweets
    if should_go_deep:
        summary = summarizer.get_results_summary(tweets, TOXICITY_THRESHOLD)
        # print('Top users:', summary.top_users)
        all_tweets.extend(
            _get_tweets_from_user_scores(summary.top_users.items(), limit)
        )
        # print('Top hashtags:', summary.top_hashtags)
        all_tweets.extend(
            _get_tweets_from_hashtag_scores(summary.top_hashtags.items(), limit)
        )
    return [data_point for data_point in yield_data_points_from_tweets(all_tweets)]


def yield_data_points_from_tweet_dicts(tweet_dicts):
    for serialized_tweet in tweet_dicts:
        if serialized_tweet['toxicity'] <= TOXICITY_THRESHOLD:
            continue
        tweet_text = serialized_tweet['text']
        source_username = serialized_tweet['user']
        hashtag_texts = []
        for hashtag_info in serialized_tweet.get('hashtags', []):
            hashtag_str = '#%s' % hashtag_info['text']
            hashtag_texts.append(hashtag_str)
            # User -> hashtag link
            yield {
                'source': 's: %s' % source_username,
                'target': '%s' % hashtag_str,
                'lt': 'create',
                'tweet': tweet_text
            }
        for tagged_user_info in serialized_tweet.get('user_mentions', []):
            mentioned_username = tagged_user_info['screen_name']
            # User -> mentioned user link
            yield {
                'source': 's: %s' % source_username,
                'target': 'm: %s' % mentioned_username,
                'lt': 'mention',
                'tweet': tweet_text
            }
            for hashtag_str in hashtag_texts:
                # Mentioned user -> hashtag link
                yield {
                    'source': 'm: %s' % mentioned_username,
                    'target': hashtag_str,
                    'lt': 'mention_with_hashtag',
                    'tweet': tweet_text
                }


def yield_data_points_from_tweets(tweets):
    # print('Generating points')
    tweet_dicts = utils.get_tweet_dicts(tweets)
    yield_data_points_from_tweet_dicts(tweet_dicts)


def _get_tweets_from_user_scores(user_scores, limit):
    all_tweets = []
    it_count = 0
    for username, score in user_scores:
        it_count += 1
        if it_count > MAX_DEPTH:
            continue
        # print('Getting data for: ', username)
        tweets, error = data_fetch_public.get_tweets_of_user(
            username, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        all_tweets.extend(tweets)
    return all_tweets


def _get_tweets_from_hashtag_scores(hashtag_scores, limit):
    it_count = 0
    all_tweets = []
    for hashtag_str, score in hashtag_scores:
        it_count += 1
        if it_count > MAX_DEPTH:
            continue
        # print('Getting hashtag data for: ', hashtag_str)
        tweets, error = data_fetch_public.get_tweets_from_search(
            hashtag_str, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        all_tweets.extend(tweets)
    return all_tweets
