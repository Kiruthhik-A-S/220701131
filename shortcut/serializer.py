from rest_framework import serializers
from .models import URLMapping, Click

class URLMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLMapping
        fields = ['original_url', 'short_url', 'created_at', 'expires_at', 'clicked']

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['clicked_at']