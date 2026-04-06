import random
import string
from urllib import request

from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse
from django.urls import reverse
from .models import urls
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'api/index.html'

class AnalyticsView(generic.ListView):
    model = urls
    template_name = 'api/analytics.html'
    context_object_name = "urls"

class RedirectView(generic.View):
    def get(self, request, short_url):
        try:
            url_info = urls.objects.get(short_url=short_url)
            url_info.used_count += 1
            url_info.save()
            return redirect(url_info.original_url)
        except urls.DoesNotExist:
            raise Http404("Short URL does not exist")

def generate_short_url():
    short_url = ""
    for x in range(6):
        short_url += random.choice(string.ascii_letters + string.digits)
    return short_url

def create_short_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:
            short_url = generate_short_url()
            url_info = urls.objects.create(original_url=original_url, short_url=short_url)
            return render(request, 'api/shortened_url.html', {'url': url_info})
        return render(request, 'api/index.html')
    
class ShortenedURLView(generic.View):
    model = urls
    template_name = 'api/shortened_url.html'
    def get(self, request, short_url):
        url_info = get_object_or_404(urls, short_url=short_url)
        return render(request, self.template_name, {'url': url_info})