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
import requests
@APi_view(['POST'])

def create_shortcut(request):
        auth_url = "http://20.244.56.144/evaluation-service/auth"

        auth_payload = {
            "email": "220701131@rajalakshmi.edu.in",
            "name": "Kiruthhik A S",
            "rollNo": "220701131",
            "accessCode": "cWyaXW",
            "clientID": "469d8fbd-c687-4f59-b80b-071db2d64575",
            "clientSecret": "AgsaCygFHXNKBmaN"
        }
        response = requests.post(auth_url, json=auth_payload)
        response.raise_for_status()

        data = response.json()
        token = data.get("access_token")  

        if not token:
            print("Token not found in response:", data)
        else:
            print("✅ Token received successfully")
            print("Token:", token)

        URL = "http://20.244.56.144/evaluation-service/logs"

        #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyMjA3MDExMzFAcmFqYWxha3NobWkuZWR1LmluIiwiZXhwIjoxNzUxNjk5MjA2LCJpYXQiOjE3NTE2OTgzMDYsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiI2MzcxODMyOS04NTIxLTRmZWUtOTZjNS0wYTg4ZmY2N2Y3MTAiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJraXJ1dGhoaWsgYSBzIiwic3ViIjoiNDY5ZDhmYmQtYzY4Ny00ZjU5LWI4MGItMDcxZGIyZDY0NTc1In0sImVtYWlsIjoiMjIwNzAxMTMxQHJhamFsYWtzaG1pLmVkdS5pbiIsIm5hbWUiOiJraXJ1dGhoaWsgYSBzIiwicm9sbE5vIjoiMjIwNzAxMTMxIiwiYWNjZXNzQ29kZSI6ImNXeWFYVyIsImNsaWVudElEIjoiNDY5ZDhmYmQtYzY4Ny00ZjU5LWI4MGItMDcxZGIyZDY0NTc1IiwiY2xpZW50U2VjcmV0IjoiQWdzYUN5Z0ZIWE5LQm1hTiJ9.bqB9LsVqzIRckLn35PqpY7y-TXTKNpFLQ3HaFn6PSWw"
        header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        body = {
                "stack":"backend",
            "level":"error",
            "package":"handler",
            "message": "received string, expected bool"
            }
        url = request.data.get('url', '')
        if not url:
            body['message'] = "URL is required"
            body['handler'] = "create_shortcut"
            respone = requests.post(URL, headers=header, json=body)
            print(respone.text)
            return Response({'error': 'URL is required'}, status=400)
        validity = request.data.get('validity', 30)
        if validity <= 0:
            body['message'] = "Validity must be a positive integer"
            body['handler'] = "create_shortcut"
            respone = requests.post(URL, headers=header, json=body)
            return Response({'error': 'Validity must be a positive integer'}, status=400)
        shortcode = request.data.get('shortcode', '')

        existing_shortcodes = URLMapping.objects.values_list('short_url', flat=True)
        if(shortcode == ""):
            shortcode = generate_short_url()
            while shortcode in existing_shortcodes:

                shortcode = generate_short_url()
        elif shortcode in existing_shortcodes:
            body['message'] = "Shortcode already exists"
            body['handler'] = "create_shortcut"
            respone = requests.post(URL, headers=header, json=body)
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
        body['message'] = "Shortcode created successfully"
        body['handler'] = "create_shortcut"
        respone = requests.post(URL, headers=header, json=body)
        print(respone.text)
        return Response(response, status=status.HTTP_201_CREATED)
    
@APi_view(['GET'])
def get_shortcut(request, shortcode):
        auth_url = "http://20.244.56.144/evaluation-service/auth"

        auth_payload = {
            "email": "220701131@rajalakshmi.edu.in",
            "name": "Kiruthhik A S",
            "rollNo": "220701131",
            "accessCode": "cWyaXW",
            "clientID": "469d8fbd-c687-4f59-b80b-071db2d64575",
            "clientSecret": "AgsaCygFHXNKBmaN"
        }
        response = requests.post(auth_url, json=auth_payload)
        response.raise_for_status()

        data = response.json()
        token = data.get("access_token")  
        URL = "http://20.244.56.144/evaluation-service/logs"
        #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyMjA3MDExMzFAcmFqYWxha3NobWkuZWR1LmluIiwiZXhwIjoxNzUxNjk3NjQwLCJpYXQiOjE3NTE2OTY3NDAsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiJhYzM3Mzg5MS0wYTg2LTRkODAtODczMy05NDFiNzhjMWUzMzgiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJraXJ1dGhoaWsgYSBzIiwic3ViIjoiNDY5ZDhmYmQtYzY4Ny00ZjU5LWI4MGItMDcxZGIyZDY0NTc1In0sImVtYWlsIjoiMjIwNzAxMTMxQHJhamFsYWtzaG1pLmVkdS5pbiIsIm5hbWUiOiJraXJ1dGhoaWsgYSBzIiwicm9sbE5vIjoiMjIwNzAxMTMxIiwiYWNjZXNzQ29kZSI6ImNXeWFYVyIsImNsaWVudElEIjoiNDY5ZDhmYmQtYzY4Ny00ZjU5LWI4MGItMDcxZGIyZDY0NTc1IiwiY2xpZW50U2VjcmV0IjoiQWdzYUN5Z0ZIWE5LQm1hTiJ9.QUO9fa3NssHd4jvSVrV-ZzwyVxRfwoUG-5Ca4tY3s4Y"
        header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        body = {
                "stack":"backend",
            "level":"error",
            "package":"handler",
            "message": "received string, expected bool"
            }
        URLmap = URLMapping.objects.get(short_url=shortcode)
        if not URLmap:
            body['message'] = "Shortcode not found"
            body['handler'] = "get_shortcut"
            requests.post(URL, headers=header, json=body)
            return Response({'error': 'Shortcode not found'}, status=404)
        URLmap.clicked += 1
        URLmap.save()
        click = Click.objects.create(
            url_mapping=URLmap,
            clicked_at=timezone.now()
        )
        click.save()

        response = URLMappingSerializer(URLmap)
        body['message'] = "Shortcode retrieved successfully"
        body['handler'] = "get_shortcut"
        #response = requests.post(URL, headers=header, json=body)
        #print(response.text)
        return Response(response.data, status=status.HTTP_200_OK)


