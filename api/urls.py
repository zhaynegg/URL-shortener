from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('analytics', views.AnalyticsView.as_view(), name='analytics'),
    path('create/', views.create_short_url, name='create_short_url'), 
    path('shortened/<str:short_url>/', views.ShortenedURLView.as_view(), name='shortened_url'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name="logout"),

    path('<str:short_url>/', views.RedirectView.as_view(), name='redirect'),
]