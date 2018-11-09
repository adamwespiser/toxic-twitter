import datetime as dt
import random
import time
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect

from data_fetch_helpers import constants as data_fetch_constants
from data_fetch_helpers import public as data_fetch_public


def home(request):
    return render(
        request,
        'clientapp/home.html',
        {
            'title': 'ToxicSense',
        }
    )


def analyze_tweets(request):
    search_term = request.GET.get('topic')
    tweets = data_fetch_public.get_tweets_from_search(
        search_term, 300, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    print('Analyzing toxicity of results')
    start = time.time()
    result = [tweet.to_dict() for tweet in tweets]
    end = time.time()
    print('Took', end - start, 'seconds')
    return JsonResponse(result, safe=False)


def analyze_user_tweets(request):
    user = request.GET.get('user')
    user_clean = re.sub("[^A-Za-z_]","",user)
    user_max_len = user_clean if len(x) < 15 else x[0:15]
    tweets = data_fetch_public.get_tweets_of_user(
        user, 100, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    print('Analyzing toxicity of results')
    start = time.time()
    result = [
        tweet.to_dict()
        for tweet in tweets
        if tweet.user == user
    ]
    end = time.time()
    print('Took', end - start, 'seconds')
    return JsonResponse(result, safe=False)
