from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Manga(models.Model):
    url = models.URLField()
    tag = models.ManyToManyField(Tags, blank=True)
    title = models.CharField(max_length=200, blank=True)
    preview_img = models.URLField(blank=True)
    description = models.TextField(blank=True)
    status = models.TextField(blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    author = models.CharField(max_length=200, blank=True)
    first_chapter = models.ForeignKey(
        "Chapter", null=True, on_delete=models.SET_NULL, related_name="first_manga"
    )
    last_chapter = models.ForeignKey(
        "Chapter", null=True, on_delete=models.SET_NULL, related_name="last_manga"
    )

    def __str__(self):
        return str(self.url)


class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    images = models.JSONField(null=True, blank=True)
    url = models.URLField()
    date = models.DateField(null=True)
    chapter_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.url)

