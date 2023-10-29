from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("api_mangas", views.api_mangas, name="api_mangas"),
    path("api_manga/<str:pk>/", views.api_manga, name="api_manga"),
    path("api_mangas_preview", views.api_mangas_preview, name="api_mangas_preview"),
]
