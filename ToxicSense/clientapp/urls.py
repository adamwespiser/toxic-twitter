from django.urls import path
from clientapp import views

urlpatterns = [
    path("", views.home, name="home"),
]