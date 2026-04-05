from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics/<int:url_id>/', views.analytics, name='analytics'),
]