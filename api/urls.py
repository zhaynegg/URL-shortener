from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('analytics/<int:url_id>/', views.analytics, name='analytics'),
    path('redirect/<str:short_url>/', views.redirect, name='redirect'),
    path('create/', views.create_short_url, name='create_short_url'),  
]