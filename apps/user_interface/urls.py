from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("settings/", views.settingsPage, name="settings"),
    path("register/", views.registerUser, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("manga/<str:title>/", views.mangaPage, name="manga"),
    path(
        "<str:manga_title>/chapter/<str:pk>/",
        views.chapterPage,
        name="chapter",
    ),
    path("library", views.library, name="library"),
    path(
        "update_manga_follow_status/<str:pk>/",
        views.update_manga_follow_status,
        name="update_manga_follow_status",
    ),
]
