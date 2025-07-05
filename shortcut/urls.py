from django.urls import path
from . import views

urlpatterns = [
    path('shortcut/', views.create_shortcut, name='create_shortcut'),
    path('shortcut/<str:shortcode>/', views.get_shortcut, name='get_shortcut'),
]