from django.shortcuts import render, redirect
from ..user_interface.forms import MangaForm
from apps.scraper.scrapers.mangatx import scrape_add_manga, scrape_chapters
import time


def scraper(request):
    context = {}
    if request.method == "POST":
        form = MangaForm(request.POST)
        if form.is_valid():
            manga = form.save(commit=False)
            url = form.cleaned_data["url"]

            time1 = time.time()
            data = scrape_add_manga(request, url)
            time2 = time.time()
            print("time taken:", time2 - time1)

            context = {"form": form, "data": data}

    else:
        form = MangaForm()

    context["form"] = form  # Make sure form is always included in the context

    return render(request, "scraper/scraper_page.html", context)


