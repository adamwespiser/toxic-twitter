import datetime as dt
import random
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import html
from toxicityanalyzer import toxicityanalyzer

from twitterscraper import query_tweets

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

def get_tweets(topic):
    tweets = query_tweets(topic, limit=1)
    tweets.reverse()
    return tweets