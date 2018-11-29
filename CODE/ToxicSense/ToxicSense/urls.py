from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("", include("clientapp.urls")),
]

urlpatterns += staticfiles_urlpatterns()