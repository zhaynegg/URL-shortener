from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from .models import urls

def index(request):
    return render(request, 'api/index.html')

def analytics(request, url_id):
    info = get_object_or_404(urls, id=url_id)
    return HttpResponse(f"This is the analytics page for URL used count: {info.used_count} where you can see the statistics of your shortened URLs")