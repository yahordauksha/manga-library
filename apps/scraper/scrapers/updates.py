from ...manga.models import Manga
from ...manga.models import Manga
from manga_project.celery import app
from .mangatx import scrape_chapters


@app.task
def get_updates():
    print("Looking for manga updates...")
    mangas = Manga.objects.all()
    for manga in mangas:
        print("Checking ", manga.title, " ...")
        scrape_chapters("str", manga.url)
