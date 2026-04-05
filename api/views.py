from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import urls

def index(request):
    return HttpResponse("Hello. This is the main page where you are going to shorten URLs")

def analytics(request, url_id):
    try:
        info = urls.objects.get(id=url_id)
        return HttpResponse(f"This is the analytics page for URL used count: {info.used_count} where you can see the statistics of your shortened URLs")  
    except urls.DoesNotExist:
        raise Http404("URL not found")