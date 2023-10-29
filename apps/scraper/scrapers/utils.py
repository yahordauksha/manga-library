from .mangatx import scrape_add_manga
from django.shortcuts import redirect, get_object_or_404
from ...manga.models import Manga
from ...manga.utils import check_manga_existence
from ...user_profile.utils import update_last_viewed_chapter
from bs4 import BeautifulSoup
import requests, datetime, time
from ...manga.models import Manga, Tags, Chapter
from manga_project.celery import app
import json
import pdb


def add_manga(form, request):
    # pdb.set_trace()
    url = form.cleaned_data["url"]

    if not check_manga_existence(url):
        scrape_add_manga(request, url)
        print("Manga successfully added.")
        return redirect("home")

    manga = get_object_or_404(Manga, url=url)

    if not manga.participants.filter(id=request.user.id).exists():
        manga.participants.add(request.user)
        manga.save()
        update_last_viewed_chapter(request.user, manga, None)
        print("The user has been added as a participant")
