from django.urls import path
from django.views.generic import TemplateView

from clientapp import views


urlpatterns = [
    path('old', views.home, name='old-home'),
    path('', views.summary, name='home'),
    path('analyze', views.analyze_topic, name='analyze_topic'),
    path('analyzeuser', views.analyze_user, name='analyze_user'),
    path('analyzetweet', views.analyze_tweet, name='analyze_tweet'),
    path("analyzetoxicity", views.analyze_toxicity, name="analyze_toxicity"),
    path('summary', views.summary, name='all_summary'),
    path('summary_api', views.summary_api, name='summary_api'),
    path('get_graph', views.get_graph, name='get_graph'),
    path('show_graph', TemplateView.as_view(template_name='clientapp/show_graph.html'))
]
