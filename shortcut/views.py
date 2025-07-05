from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view as APi_view
# Create your views here.
from rest_framework.response import Response
from .utils import generate_short_url
from .models import URLMapping,Click
from .serializer import URLMappingSerializer, ClickSerializer
from rest_framework import status
from django.utils import timezone
@APi_view(['POST'])
def create_shortcut(request):
        url = request['POST'].get('url', '')
        if not url:
            return Response({'error': 'URL is required'}, status=400)
        validity = request['POST'].get('validity', 30)
        if validity <= 0:
            return Response({'error': 'Validity must be a positive integer'}, status=400)
        shortcode = request['POST'].get('shortcode', '')

        existing_shortcodes = URLMapping.objects.values_list('short_url', flat=True)
        if(shortcode == ""):
            shortcode = generate_short_url()
            while shortcode in existing_shortcodes:
                shortcode = generate_short_url()
        elif shortcode in existing_shortcodes:
            return Response({'error': 'Shortcode already exists'}, status=400)
        created_at = timezone.now()
        expires_at = created_at + timezone.timedelta(minutes=validity)
        url_mapping = URLMapping.objects.create(
            original_url=url,
            short_url=shortcode,
            created_at=created_at,
            expires_at=expires_at
        )
        response = {
            "shortLink" : "https://8000/"+shortcode,
            "expiry" : expires_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
@APi_view(['GET'])
def get_shortcut(request, shortcode):
        URLmap = URLMapping.objects.get(short_url=shortcode)
        if not URLmap:
            return Response({'error': 'Shortcode not found'}, status=404)
        URLmap.clicked += 1
        URLmap.save()
        click = Click.objects.create(
            url_mapping=URLmap,
            clicked_at=timezone.now()
        )
        click.save()

        response = URLMappingSerializer(URLmap)

        return Response(response.data, status=status.HTTP_200_OK)


