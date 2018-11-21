from django.urls import path
from clientapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze", views.analyze_topic, name="analyze_topic"),
    path("analyzeuser", views.analyze_user, name="analyze_user"),
    path("analyzetweet", views.analyze_tweet, name="analyze_tweet"),
]