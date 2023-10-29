from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.user_interface.urls")),
    # Dev urls
    path("scraper/", include("apps.scraper.urls")),
    path("manga/", include("apps.manga.urls")),
    path("user_profile/", include("apps.user_profile.urls")),
]
