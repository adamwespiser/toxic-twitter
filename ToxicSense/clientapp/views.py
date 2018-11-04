import datetime as dt
import random
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
    result = [tweet.to_dict() for tweet in tweets]
    return JsonResponse(result, safe=False)


def analyze_user_tweets(request):
    user = request.GET.get('user')
    tweets = data_fetch_public.get_tweets_of_user(
        user, 100, data_fetch_constants.DATA_SOURCE_TWEEPY
    )
    result = [
        tweet.to_dict()
        for tweet in tweets
        if tweet.user == user
    ]
    return JsonResponse(result, safe=False)
