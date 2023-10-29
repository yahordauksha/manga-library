from .models import Manga


def check_manga_existence(url):
    return Manga.objects.filter(url=url).exists()
