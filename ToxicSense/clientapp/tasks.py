from __future__ import absolute_import, unicode_literals
from celery import task
import logging
import sys
import time
import pytz
from datetime import datetime

from django.utils import html

import requests

from clientapp.models import Tweet, Topic
from data_fetch_helpers import constants as data_fetch_constants
from data_fetch_helpers import public as data_fetch_public

logger = logging.getLogger('toxicsense.clientapp.tasks')


@task(time_limit=600)
def collect_top_trends():
    trends, error = data_fetch_public.get_top_trends(data_fetch_constants.DATA_SOURCE_TWEEPY)
    if error:
        return
    for i in range(len(trends[:10])):
        name = trends[i]['name']
        logger.info("Getting tweets for " + name)
        start = time.time()
        tweets, error = data_fetch_public.get_tweets_from_search(name, 300, data_fetch_constants.DATA_SOURCE_TWEEPY)
        if error:
            continue
        result = [_get_tweet_dict(tweet) for tweet in tweets]
        try:
            _update_database(name, result)
        except:
            logger.exception(sys.exc_info())
            continue
        end = time.time()
        logger.info('Took ' + str(end - start) + ' seconds')


@task(time_limit=20)
def update_database(search_term, tweets):
    logger.info('Storing results in database')
    start = time.time()
    _update_database(search_term, tweets)
    end = time.time()
    logger.info('Took ' + str(end - start) + ' seconds')


def _update_database(search_term, tweets):
    for item in tweets:
        localized_timestamp = pytz.utc.localize(datetime.strptime(item['timestamp'], data_fetch_constants.OUR_DATETIME_FORMAT))
        tweet_obj, created = Tweet.objects.get_or_create(tweet_id=item['id'], screen_name=item['user'], text=item['text'], created_at=localized_timestamp, toxicity=item['toxicity'])
        tweet_obj.save()
        topic_obj, created = Topic.objects.get_or_create(topic_term=search_term, tweet=tweet_obj)
        topic_obj.save()


def _get_tweet_dict(tweet):
    return {
        'id': tweet.id,
        'user': tweet.user,
        'timestamp': tweet.timestamp,
        'text': html.escape(tweet.text),
        'toxicity': _get_toxicity(tweet.text)
    }


def _get_toxicity(text):
    BASE_URL = 'http://localhost:8000'
    URL = '{}/analyzetoxicity'.format(BASE_URL)
    r = requests.post(URL, data = {'text': text})
    response_data = r.json()
    score = response_data['score']
    return score
