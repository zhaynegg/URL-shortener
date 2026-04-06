from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('analytics', views.AnalyticsView.as_view(), name='analytics'),
    path('redirect/<str:short_url>/', views.RedirectView.as_view(), name='redirect'),
    path('create/', views.create_short_url, name='create_short_url'), 
    path('shortened/<str:short_url>/', views.ShortenedURLView.as_view(), name='shortened_url'),
]