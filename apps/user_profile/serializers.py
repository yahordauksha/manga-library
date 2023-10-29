from django.contrib.auth.models import User
from .models import UserMangaHistory
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserMangaHistorySerializer(ModelSerializer):
    class Meta:
        model = UserMangaHistory
        fields = "__all__"
