from collections import namedtuple
from collections import OrderedDict 
from operator import itemgetter

from clientapp import constants


ResultsSummary = namedtuple(
    'ResultsSummary',
    [
        'toxic_tweets', 'benign_tweets',
        'top_hashtags', 'top_users', 'top_mentioned_users',
        'toxic_tweet_count', 'total_tweets', 'toxicity_percentage', 'safe_score',
        'toxic_user_count', 'total_users', 'user_toxicity_percentage'
    ]
)


def get_results_summary(tweets, toxicity_threshold=constants.TOXICITY_THRESHOLD):
    if not tweets:
        return None
    result = [tweet.to_dict() for tweet in tweets]
    result = sorted(result, key=itemgetter('toxicity')) 
    top_toxic_users = {}
    top_toxic_mentioned_users = {}
    top_toxic_hashtags = {}
    total_tweets = len(result)
    toxic_tweet_count = 0
    toxic_tweets = []
    non_toxic_tweets = []
    for item in result:
        toxicity = item['toxicity']
        username = item['user']
        if toxicity <= toxicity_threshold:
            top_toxic_users[username] = top_toxic_users.get(username, 0)
            non_toxic_tweets.append(item)
            continue
        toxic_tweets.append(item)
        toxic_tweet_count += 1
        toxicity_adder = 1 * toxicity
        top_toxic_users[username] = top_toxic_users.get(username, 0) + toxicity_adder
        for tagged_user_info in item.get('user_mentions', []):
            username = tagged_user_info['screen_name']
            top_toxic_mentioned_users[username] = top_toxic_mentioned_users.get(username, 0) + toxicity_adder
        for hashtag_info in item.get('hashtags', []):
            hashtag_str = hashtag_info['text']
            top_toxic_hashtags[hashtag_str] = top_toxic_hashtags.get(hashtag_str, 0) + toxicity_adder
    
    ordered_top_hashtags = OrderedDict(
        sorted(top_toxic_hashtags.items(), key=lambda x: x[1], reverse=True)[:10]
    )
    toxic_only_users = [
        (username, toxicity)
        for username, toxicity in top_toxic_users.items()
        if toxicity > 0
    ]
    ordered_top_users = OrderedDict(
        sorted(toxic_only_users, key=lambda x: x[1], reverse=True)[:10]
    )
    ordered_top_mentioned_users = OrderedDict(
        sorted(top_toxic_mentioned_users.items(), key=lambda x: x[1], reverse=True)[:10]
    )
    toxic_user_count = sum([
        1 if value > 0 else 0
        for value in top_toxic_users.values()
    ])
    toxic_tweets.reverse()
    total_users = len(top_toxic_users)
    user_toxicity_percentage = (toxic_user_count / float(total_users)) * 100
    toxicity_percentage = (toxic_tweet_count / float(total_tweets)) * 100
    safe_score = int(100 - toxicity_percentage)
    return ResultsSummary(
        toxic_tweets, non_toxic_tweets,
        ordered_top_hashtags, ordered_top_users, ordered_top_mentioned_users,
        toxic_tweet_count, total_tweets, toxicity_percentage, safe_score,
        toxic_user_count, total_users, user_toxicity_percentage
    )
