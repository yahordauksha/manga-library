from .models import Manga
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MangaSerializer, UserMangaHistorySerializer
from ..user_profile.models import UserMangaHistory
from rest_framework import status


@api_view(["GET"])
def api_mangas(request):
    mangas = Manga.objects.all()
    serializer = MangaSerializer(mangas, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def api_manga(request, pk):
    manga = Manga.objects.filter(pk=pk)
    serializer = MangaSerializer(manga, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def api_mangas_preview(request):
    # Get the currently logged-in user
    user = request.user

    # Retrieve the user's manga history
    user_history = UserMangaHistory.objects.filter(user=user)

    # Serialize the user's manga history data
    serializer = UserMangaHistorySerializer(user_history, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
