from django.db import models

# Create your models here.
class urls(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users', on_delete=models.CASCADE, null=True, blank=True)
    used_count = models.IntegerField(default=0)

    def __str__(self):
        return self.short_url

class users(models.Model):
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username