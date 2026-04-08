import random
import string
import xxhash
from urllib import request

from django.shortcuts import redirect, render, get_object_or_404
from .mixins import SupabaseLoginRequiredMixin
from django.http import Http404, HttpResponse
from django.urls import reverse
from .models import urls
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .supabase_client import supabase
from django.contrib import messages

def login_view(request):
    if request.session.get("supabase_access_token"):
        return redirect("api:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if not response.session:
                messages.error(request, "Invalid credentials")
                return render(request, "api/login.html")
            
            if not response.user:
                messages.error(request, "Invalid credentials")
                return render(request, "api/login.html")

            if not response.user.confirmed_at:
                messages.error(request, "Please confirm your email first")
                return render(request, "api/login.html")
            user = response.user
            session = response.session
            
            nw_response = (
                supabase.table("profile")
                .select("username")
                .eq("id", user.id)
                .maybe_single()
                .execute()
            )

            if not nw_response.data:
                messages.error(request, "No such user")
                return render(request, "api/login.html")

            username = nw_response.data["username"]
            request.session["user_email"] = email
            request.session["username"] = username
            request.session["supabase_access_token"] = session.access_token
            return redirect('api:index')
        except Exception as e:
            return render(request, 'api/login.html', {'error': str(e)})
    return render(request, "api/login.html")


def registration_view(request):
    if request.session.get("supabase_access_token"):
        return redirect("api:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            user = response.user
            if not user:
                raise Exception("User creation failed")
            
            supabase.table("profile").insert({
                    "id": user.id,
                    "username": username,
            }).execute()
            return redirect('api:login')
        except Exception as e:
            return render(request, 'api/register.html', {'error': str(e)})
        
    return render(request, "api/register.html")

def logout_view(request):
    request.session.flush()
    return redirect('api:login')

class IndexView(SupabaseLoginRequiredMixin, generic.TemplateView):
    template_name = 'api/index.html'
        


class AnalyticsView(SupabaseLoginRequiredMixin, generic.ListView):
    model = urls
    template_name = 'api/analytics.html'
    context_object_name = 'urls'
    def get_queryset(self):
        current_username = self.request.session.get("username")
        query = urls.objects.filter(user_username=current_username)
        for url in query:
            url.short_url = self.request.build_absolute_uri(f'{url.short_url}')

        return query


class RedirectView(generic.View):
    def get(self, request, short_url):
        try:
            url_info = urls.objects.get(short_url=short_url)
            url_info.used_count += 1
            url_info.save()
            return redirect(url_info.original_url)
        except urls.DoesNotExist:
            raise Http404("Short URL does not exist")

def generate_short_url(original_url):
    short_url = xxhash.xxh3_128_hexdigest(original_url)[:8]
    while urls.objects.filter(short_url = short_url).exists():
        original_url += random.choice(string.ascii_letters + string.digits)
        short_url = xxhash.xxh3_128_hexdigest(original_url)[:8]
    return short_url

def create_short_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:
            if urls.objects.filter(original_url = original_url).exists():
                url_info = urls.objects.get(original_url = original_url)
            else:
                short_url = generate_short_url(original_url)
                url_info = urls.objects.create(original_url=original_url, short_url=short_url, user_username=request.session["username"])
                url_info.short_url = request.build_absolute_uri(f'/{url_info.short_url}')
            return render(request, 'api/shortened_url.html', {'url': url_info})
        
        return render(request, 'api/index.html')
    
class ShortenedURLView(SupabaseLoginRequiredMixin, generic.View):
    model = urls
    template_name = 'api/shortened_url.html'
    def get(self, request, short_url):
        url_info = get_object_or_404(urls, short_url=short_url)
        url_info.short_url = request.build_absolute_uri(f'/{url_info.short_url}')
        return render(request, self.template_name, {'url': url_info})