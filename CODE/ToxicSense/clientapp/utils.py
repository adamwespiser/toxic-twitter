import re


def get_user_tweet_id_from_tweet_url(tweet_url):
    # tweet_url is in the format https://twitter.com/username/status/1064734907940994497
    url_fragments = tweet_url.rstrip('/').rsplit('/', 3)
    tweet_id = url_fragments[-1]
    user = url_fragments[-3]
    return (user, tweet_id)


def get_clean_username(user):
    user_clean = re.sub("[^A-Za-z_]", "", user)
    user_clean = user_clean if len(user_clean) < 15 else user_clean[0:15]
    return user_clean


def get_tweet_dicts(tweets):
    return [tweet.to_dict() for tweet in tweets]
