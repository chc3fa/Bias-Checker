from django.shortcuts import render
from django.http import JsonResponse
from newsapi import NewsApiClient
import pycountry

# Create your views here.
newsapi = NewsApiClient(api_key='309a701bb29e4512b592a52ddb0952d4')

def get_country_name(alpha_2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_code)
        return country.name
    except:
        return alpha_2_code
    
def get_articles_for_country(request, country_code):
    country_name = get_country_name(country_code)

    if not country_name:
        return JsonResponse({'error': 'Invalid country code.'}, status=400)
    
    try:
        articles = newsapi.get_everything(q=country_name, language='en', sort_by='relevancy', page_size=100)
        return JsonResponse(articles)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)