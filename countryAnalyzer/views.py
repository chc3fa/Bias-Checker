from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import requests
import pycountry
from textblob import TextBlob

def get_country_name(alpha_2_code):
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_code)
        return country.name
    except:
        return alpha_2_code

def analyze_news(request, country):
    country_name = get_country_name(country)
    if not country_name:
        return HttpResponse("Invalid country code.")
    news_url = reverse('get_articles_for_country', args=[country])
    full_url = request.build_absolute_uri(news_url)

    response = requests.get(full_url)
    news_data = response.json()

    combined_news =  " ".join(article["content"] for article in news_data["articles"])

    blob = TextBlob(combined_news)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    sentiment = "Neutral"
    if polarity > 0.05:
        sentiment="Positive"
    elif polarity <= 0.05:
        sentiment="Negative"

    return render(request, 'analysis.html', {
        "country": country_name,
        "sentiment": sentiment,
        "polarity": "{:.3f}".format(polarity * 10),
        "subjectivity": "{:.3f}".format(subjectivity)
    })

    # return JsonResponse({
    #         "country": country_name,
    #         "sentiment": sentiment,
    #         "polarity": polarity - 0.05,
    #         "subjectivity": subjectivity
    # })
