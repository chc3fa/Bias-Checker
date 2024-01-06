from django.urls import path
from .views import analyze_news

urlpatterns = [
    path('analyze-news/<str:country>/', analyze_news, name='analyze-news'),
]

