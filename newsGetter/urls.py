from django.urls import path
from . import views

urlpatterns = [
    path('articles/<str:country_code>/', views.get_articles_for_country, name='get_articles_for_country'),
]