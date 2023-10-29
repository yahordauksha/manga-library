from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, OuterRef, Subquery
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.db.models import Prefetch, Count
import pdb
from unidecode import unidecode

from .forms import MangaForm
from ..scraper.scrapers.mangatx import scrape_add_manga
from ..scraper.scrapers.utils import add_manga
from ..scraper.scrapers.updates import get_updates
from ..manga.models import Manga, Chapter
from ..user_profile.models import UserMangaHistory
from ..manga.utils import check_manga_existence
from ..user_profile.utils import update_last_viewed_chapter


def home(request):
    context = {}
    form = MangaForm(request.POST or None)

    if request.method == "POST":
        action = request.POST.get("value")

        POST_functions(request, action, "home", form, "", "")

    if request.user.is_authenticated:
        mangas = Manga.objects.filter(participants=request.user)
        mangas = mangas.filter(usermangahistory__follow_updates=True)

        mangas = mangas.annotate(
            last_view_chapter=Subquery(
                UserMangaHistory.objects.filter(
                    user=request.user, manga=OuterRef("pk"), follow_updates=True
                ).values("last_view_chapter")[:1]
            )
        )

        context["mangas"] = mangas

    context["form"] = form

    return render(request, "user_interface/home.html", context)


def library(request):
    context = {}
    form = MangaForm(request.POST or None)

    search_query = request.GET.get("q")

    if request.method == "POST":
        action = request.POST.get("value")

        POST_functions(request, action, "library", form, "", "")

    if request.user.is_authenticated:
        mangas = Manga.objects.filter(participants=request.user)

        # Check if a search query is provided and filter the results accordingly
        if search_query:
            mangas = mangas.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query)
            )

        mangas = mangas.annotate(
            last_view_chapter=Subquery(
                UserMangaHistory.objects.filter(
                    user=request.user, manga=OuterRef("pk")
                ).values("last_view_chapter")[:1]
            )
        )
        context["mangas"] = mangas

    context["form"] = form

    return render(request, "user_interface/library.html", context)


def settingsPage(request):
    context = {}
    return render(request, "user_interface/settings.html", context)


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "User OR password does not exist.")

    context = {"page": page}
    return render(request, "user_interface/login_register.html", context)


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")


def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        print("user trys to register")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured, you stoopid")

    context = {"form": form}
    return render(request, "user_interface/login_register.html", context)


def mangaPage(request, title):
    form = MangaForm(request.POST or None)
    manga = Manga.objects.get(title=title)
    chapters = Chapter.objects.filter(manga=manga).order_by("-id")
    history = UserMangaHistory.objects.get(manga=manga, user=request.user)
    follow_updates = history.follow_updates

    if request.method == "POST":
        action = request.POST.get("value")

        POST_functions(request, action, "manga", form, manga, title)

    context = {
        "manga": manga,
        "chapters": chapters,
        "history": history,
        "follow_updates": follow_updates,
        "form": form,
    }
    return render(request, "user_interface/manga.html", context)


@require_POST
def update_manga_follow_status(request, pk):
    print("Update thing started...")
    manga = get_object_or_404(Manga, pk=pk)
    user_history = UserMangaHistory.objects.filter(
        manga=manga, user=request.user
    ).first()

    # Decode from JSON to boolean
    data_json = request.body
    data_string = data_json.decode("utf-8")
    data = json.loads(data_string)

    # Access the "follow_updates" value
    follow_updates = data["follow_updates"]

    try:
        follow_updates = data.get("follow_updates")
        user_history.follow_updates = follow_updates
        user_history.save()
        print("followed updates sucesfully")
        return JsonResponse(
            {
                "message": "Follow status updated successfully",
                "follow_updates": follow_updates,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def chapterPage(request, manga_title, pk):
    chapter = get_object_or_404(Chapter, id=pk)
    manga = chapter.manga
    images = json.loads(chapter.images)
    update_last_viewed_chapter(request.user, manga, chapter)

    # Get the previous chapter (if it exists)
    previous_chapter = (
        Chapter.objects.filter(manga=manga, chapter_id=(chapter.chapter_id - 1)).first()
        if chapter.chapter_id > 1
        else None
    )

    # Get the next chapter (if it exists)
    next_chapter = Chapter.objects.filter(
        manga=manga, chapter_id=(chapter.chapter_id + 1)
    ).first()

    context = {
        "chapter": chapter,
        "manga": manga,
        "images": images,
        "previous_chapter": previous_chapter,
        "next_chapter": next_chapter,
    }
    return render(request, "user_interface/chapter.html", context)


def POST_functions(request, action, page, form, manga, title):
    # pdb.set_trace()
    print("Action: ", action)

    if action == "add_manga" and form.is_valid():
        add_manga(form, request)
        return redirect("library")

    elif action == "reset-last-chapter":
        history = UserMangaHistory.objects.get(manga=manga, user=request.user)
        history.last_view_chapter = None
        history.save()
        return redirect("manga", title=title)

    elif action == "delete_manga":
        manga_id = request.POST.get("manga_id")
        manga = get_object_or_404(Manga, pk=manga_id)
        manga.participants.remove(request.user)
        history = UserMangaHistory.objects.get(manga=manga, user=request.user)
        history.last_view_chapter = None
        history.save()
        return redirect("library")

    elif action == "refresh_mangas":
        print("checking for updates")
        get_updates.delay()
        return redirect("library")
