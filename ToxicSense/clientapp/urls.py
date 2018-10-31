from django.urls import path
from clientapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze", views.analyze_tweets, name="analyze_tweets"),
    path("analyzeuser", views.analyze_user_tweets, name="analyze_user_tweets"),
]