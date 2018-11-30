import datetime as dt
import logging
import random
import re
import sys
import time
from operator import itemgetter
from collections import OrderedDict 

from django.conf import settings
from django.db.models import Avg
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from clientapp import constants
from clientapp import summarizer
from clientapp import generate_graph
from clientapp import utils
from clientapp.models import Tweet, Topic
from clientapp.tasks import update_database
from data_fetch_helpers import constants as data_fetch_constants
from data_fetch_helpers import public as data_fetch_public
from toxicityanalyzer import toxicityanalyzer


logger = logging.getLogger('toxicsense.clientapp.views')


TYPE_USER = 1
TYPE_TOPIC = 2
TYPE_CONVERSATION = 3


def home(request):
    return render(
        request,
        'clientapp/home.html',
        {
            'title': 'ToxicSense',
        }
    )


def analyze_topic(request):
    search_term = request.GET.get('topic')
    tweets, error = data_fetch_public.get_tweets_from_search(
        search_term, 300, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    if error:
        return JsonResponse({
            'error': error
        }, safe=False)
    logger.info('Analyzing toxicity of results')
    start = time.time()
    result = [tweet.to_dict() for tweet in tweets]
    end = time.time()
    logger.info('Took ' + str(end - start) + ' seconds')
    _update_database(search_term, result)
    return JsonResponse(result, safe=False)


def analyze_user(request):
    user = request.GET.get('user')
    user_clean = utils.get_clean_username(user)
    tweets, error = data_fetch_public.get_tweets_of_user(
        user_clean, 100, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    if error:
        return JsonResponse({
            'error': error
        }, safe=False)
    logger.info('Analyzing toxicity of results')
    start = time.time()
    result = [
        tweet.to_dict()
        for tweet in tweets
        if tweet.user == user
    ]
    end = time.time()
    logger.info('Took ' + str(end - start) + ' seconds')
    return JsonResponse(result, safe=False)


def analyze_tweet(request):
    url = request.GET.get('tweet_url')
    try:
        # We except it to be of form https://twitter.com/username/status/1064734907940994497
        url_fragments = url.rstrip('/').rsplit('/', 3)
        tweet_id = url_fragments[-1]
        user = url_fragments[-3]
    except:
        return JsonResponse({
            'error': True
        }, safe=False)
    replies, error = data_fetch_public.get_replies_of_tweet(
        tweet_id, user, 100, data_fetch_constants.DATA_SOURCE_TWITTER_API
    )
    if error:
        return JsonResponse({
            'error': error
        }, safe=False)
    logger.info('Analyzing toxicity of results')
    start = time.time()
    result = [
        reply.to_dict()
        for reply in replies
    ]
    end = time.time()
    logger.info('Took ' + str(end - start) + ' seconds')
    return JsonResponse(result, safe=False)


def get_graph(request):
    # return JsonResponse(constants.GRAPH_POINTS_SAMPLE, safe=False)
    search_term = request.GET.get('topic')
    tweet_url = request.GET.get('tweet_url')
    username = request.GET.get('user')
    limit = int(request.GET.get('limit', 20))
    if search_term:
        graph_data_points = generate_graph.get_graph_for_topic(search_term, limit=limit)
    elif tweet_url:
        try:
            user, tweet_id = utils.get_user_tweet_id_from_tweet_url(tweet_url)
        except:
            return JsonResponse({
                'error': True
            }, safe=False)
        graph_data_points = generate_graph.get_graph_for_tweet(user, tweet_id, limit=limit)
    elif username:
        graph_data_points = generate_graph.get_graph_for_user(username, limit=limit)
    else:
        graph_data_points = []
    return JsonResponse(graph_data_points, safe=False)


def summary(request):
    search_term = request.GET.get('topic')
    tweet_url = request.GET.get('tweet_url')
    username = request.GET.get('user')
    limit = int(request.GET.get('limit', 50))
    error = False
    tweets = []
    about = None
    analysis_type = TYPE_USER
    if search_term:
        tweets, error = data_fetch_public.get_tweets_from_search(
            search_term, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        about = 'Topic: %s' % search_term
        analysis_type = TYPE_TOPIC
    elif tweet_url:
        try:
            user, tweet_id = utils.get_user_tweet_id_from_tweet_url(tweet_url)
        except:
            return render(request, 'clientapp/error.html', {})
        tweets, error = data_fetch_public.get_replies_of_tweet(
            tweet_id, user, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        about = 'User: %s; Tweet: %s' % (user, tweet_id)
        analysis_type = TYPE_CONVERSATION
    elif username:
        tweets, error = data_fetch_public.get_tweets_of_user(
            username, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        about = 'User: %s' % username
        analysis_type = TYPE_USER
    else:
        context = {
            'homeresult': {
                'top_trends': _get_top_trends_data(),
                'top_searches': _get_top_searches_data(),
            }
        }
        return render(request, 'clientapp/summary.html', context)
    if error:
        return render(request, 'clientapp/error.html', {})
    return _render_results_with_summary(request, about, analysis_type, search_term, tweets)


def summary_api(request):
    tweets = _get_tweets_based_on_request(request)
    summary = summarizer.get_results_summary(tweets)
    return JsonResponse(summary._asdict(), safe=False)


@csrf_exempt
def analyze_toxicity(request):
    text = request.POST.get('text')
    result = {
        'score': toxicityanalyzer.get_toxicity(text)
    }
    return JsonResponse(result, safe=False)


def _render_results_with_summary(request, about, analysis_type, search_term, tweets):
    tweet_dicts = utils.get_tweet_dicts(tweets)
    summary = summarizer.get_results_summary_from_dicts(tweet_dicts)
    first_graph_points = [
        data_point for data_point in generate_graph.yield_data_points_from_tweet_dicts(tweet_dicts)
    ]
    if analysis_type == TYPE_TOPIC:
        try:
            _update_database(search_term, tweet_dicts)
        except:
            logger.exception(sys.exc_info())
    context = {
        'result': tweet_dicts,
        'about': about,
        'analysis_type': analysis_type,
        'non_toxicity_percentage': 100 - summary.toxicity_percentage if summary else 0,
        'graph_data_points': first_graph_points
    }
    if summary:
        context.update(summary._asdict())
    return render(
        request,
        'clientapp/summary.html',
        context
    )


def _get_top_trends_data():
    trends, error = data_fetch_public.get_top_trends(data_fetch_constants.DATA_SOURCE_TWEEPY)
    return [] if error else trends[:10]


def _get_top_searches_data():
    top_searches = {}
    top_topics = Topic.objects.order_by('-id')[:10]
    for topic in top_topics:
        top_searches[topic] = int(topic.tweets.all().aggregate(avg_toxicity=Avg('toxicity'))['avg_toxicity'] * 100)
    return top_searches


def _get_tweets_based_on_request(request):
    search_term = request.GET.get('topic')
    tweet_url = request.GET.get('tweet_url')
    username = request.GET.get('user')
    limit = int(request.GET.get('limit', 50))
    if search_term:
        tweets, error = data_fetch_public.get_tweets_from_search(
            search_term, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        return tweets
    elif tweet_url:
        try:
            user, tweet_id = utils.get_user_tweet_id_from_tweet_url(tweet_url)
        except:
            return render(request, 'clientapp/error.html', {})
        tweets, error = data_fetch_public.get_replies_of_tweet(
            tweet_id, user, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        return tweets
    elif username:
        tweets, error = data_fetch_public.get_tweets_of_user(
            username, limit, data_fetch_constants.DATA_SOURCE_TWEEPY
        )
        return tweets
    return None


def _update_database(search_term, result):
    if settings.ENABLE_CELERY:
        update_database.delay(search_term, result)
