import datetime as dt
import random
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import html
from toxicityanalyzer import toxicityanalyzer

from twitterscraper.query import query_tweets, query_tweets_from_user

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
    tweets = get_tweets(search_term)
    result = []
    for tweet in tweets:
        result.append({
            'user': tweet.user,
            'timestamp': tweet.timestamp,
            'text': html.escape(tweet.text),
            'toxicity': toxicityanalyzer.get_toxicity(tweet.text)
        })
    return JsonResponse(result, safe=False)

def analyze_user_tweets(request):
    user = request.GET.get('user')
    tweets = get_tweets_from_user(user)
    result = []
    for tweet in tweets:
        if tweet.user == user:
            result.append({
                'user': tweet.user,
                'timestamp': tweet.timestamp,
                'text': html.escape(tweet.text),
                'toxicity': toxicityanalyzer.get_toxicity(tweet.text)
            })
    return JsonResponse(result, safe=False)

def get_tweets(topic):
    tweets = query_tweets(topic, limit=2000)
    tweets.reverse()
    return tweets

def get_tweets_from_user(user):
    tweets = query_tweets_from_user(user, limit=2000)
    tweets.reverse()
    return tweets
