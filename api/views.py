from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from .models import urls

def index(request):
    return render(request, 'api/index.html')

def analytics(request, url_id):
    info = get_object_or_404(urls, id=url_id)
    return HttpResponse(f"This is the analytics page for URL used count: {info.used_count} where you can see the statistics of your shortened URLs")

def redirect(request, short_url):
    try:
        url_info = urls.objects.get(short_url=short_url)
        url_info.used_count += 1
        url_info.save()
        return render(request, 'api/redirect.html', {'original_url': url_info.original_url})
    except urls.DoesNotExist:
        raise Http404("Short URL does not exist") 
    
def create_short_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('longurl')
        if original_url:
            url_info = urls.objects.create(original_url=original_url)
            return HttpResponse(f"Short URL created: {request.build_absolute_uri('/')}{url_info.short_url}")
    return render(request, 'api/index.html')