from django.contrib import admin

# Register your models here.
from .models import urls, users
admin.site.register(urls)
admin.site.register(users)