from django.db import models



# Create your models here.


class URLMapping(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    clicked = models.IntegerField(default=0)

class Click(models.Model):
    url_mapping = models.ForeignKey(URLMapping, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.url_mapping.short_url} at {self.clicked_at}"