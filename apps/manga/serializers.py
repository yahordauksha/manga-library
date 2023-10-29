from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Manga
from ..user_profile.models import UserMangaHistory


class MangaSerializer(ModelSerializer):
    class Meta:
        model = Manga
        fields = "__all__"


class UserMangaHistorySerializer(ModelSerializer):
    corresponding_manga = SerializerMethodField()

    class Meta:
        model = UserMangaHistory
        fields = "__all__"

    def get_corresponding_manga(self, obj):
        # Retrieve the corresponding Manga object for the UserMangaHistory
        return {
            "manga_title": obj.manga.title,
            "manga_description": obj.manga.description,
            # Include any other fields you want from the Manga model
        }
