from django.db import models

# Create your models here.
class urls(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_username = models.CharField(max_length=150, null=False)
    used_count = models.IntegerField(default=0)

    def __str__(self):
        return self.short_url