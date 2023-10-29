from bs4 import BeautifulSoup
import requests, datetime, time
from ...manga.models import Manga, Tags, Chapter
from manga_project.celery import app
import json
import re
from ...user_profile.utils import update_last_viewed_chapter
import pdb


def scrape_add_manga(request, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    raw_html = requests.get(url, headers=headers)
    content = BeautifulSoup(raw_html.text, "html.parser")

    # scrape data
    title = content.find("div", class_="post-title").text.strip()
    description = content.find("div", class_="summary__content show-more").text.strip()
    author = content.find("div", class_="author-content").text.strip()
    tags_text = content.find("div", class_="genres-content").text.strip()
    preview_img = content.find("div", class_="summary_image").find("img")["data-src"]

    # split tags and make a list
    tags_list = [tag.strip() for tag in tags_text.split(",")] if tags_text else []

    # save manga
    manga = Manga(
        url=url,
        title=title,
        preview_img=preview_img,
        description=description,
        author=author,
        status="",
    )

    manga.save()
    manga.participants.add(request.user)
    manga.save()
    update_last_viewed_chapter(request.user, manga, None)
    print("the manga was saved succesfully")

    # save tags if they dont exist already, and make it associated to the manga
    for tag_text in tags_list:
        tag, created = Tags.objects.get_or_create(tag=tag_text)
        manga.tag.add(tag)

    scrape_chapters.delay("str", url)

    # delete this later if not needed
    return manga


@app.task
def scrape_chapters(request, url):
    print("Scrape_chapters sarted...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    raw_html = requests.get(url, headers=headers)
    content = BeautifulSoup(raw_html.text, "html.parser")
    chapters_div = content.find("div", class_="page-content-listing single-page")

    if chapters_div:
        # Get the chapters list and reverse it so we start from first chapter
        chapters = reversed(chapters_div.find_all("li", class_="wp-manga-chapter"))

        # Gettig the last chapter ID
        manga = Manga.objects.get(url=url)
        last_chapter = (
            Chapter.objects.filter(manga=manga).order_by("-chapter_id").first()
        )
        if last_chapter is not None:
            last_chapter_id = last_chapter.chapter_id
        else:
            last_chapter_id = 0

        chapter_id = last_chapter_id

        # Iterate through each chapter and scrape data
        for chapter in chapters:
            # Get the chapter URL
            chapter_url = chapter.find("a")["href"]

            # Check if this chapter already exists in the database
            if not Chapter.objects.filter(url=chapter_url).exists():
                # Scraping chapter data
                title = chapter.find("a").text.strip()

                # Images shenanigans
                image_links = image_url_scraping(chapter_url)

                # Date shenanigans
                chapter_date = date_scraping(chapter)

                chapter_id = chapter_id + 1
                # Save the chapter data
                save_chapter(
                    url, title, chapter_url, chapter_date, image_links, chapter_id
                )

                # print(f"Scraped {title}")

    else:
        print("Chapter data not found.")


def image_url_scraping(chapter_url):
    print("Getting image urls ready...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    raw_img_html = requests.get(chapter_url, headers=headers)
    content_img = BeautifulSoup(raw_img_html.text, "html.parser")
    divs = content_img.find_all("div", class_="page-break no-gaps")
    image_links = []
    for div in divs:
        img_tag = div.find("img", class_="wp-manga-chapter-img")
        if img_tag and "data-src" in img_tag.attrs:
            image_link = img_tag["data-src"].strip()
            image_links.append(image_link)
    return image_links


def date_scraping(chapter):
    date_text_element = chapter.find("span", class_="chapter-release-date")
    try:
        date_text = date_text_element.find("i").text.strip()
        # Convert the date text to a date object (you may need to adjust the date format)
        chapter_date = datetime.datetime.strptime(date_text, "%B %d, %Y").date()
    except (AttributeError, ValueError):
        chapter_date = None
    return chapter_date


def save_chapter(manga_url, title, chapter_url, chapter_date, images, chapter_id):
    print(f"Saving chapter {chapter_id}...")

    manga = Manga.objects.get(url=manga_url)

    try:
        images_json = json.dumps(images)
    except json.JSONDecodeError as e:
        print(f"JSON encoding error: {e}")
        images_json = None

    # Create new chapter
    chapter = Chapter(
        manga=manga,
        title=title,
        images=images_json,
        url=chapter_url,
        date=chapter_date,
        chapter_id=chapter_id,
    )
    chapter.save()

    # Set last and first chapters in manga
    if not manga.first_chapter:
        manga.first_chapter = chapter

    manga.last_chapter = chapter
    manga.save()

    # print(f"Saved: {title}")
