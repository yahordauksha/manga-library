from django.db import models
from ..manga.models import Manga, Chapter
from django.contrib.auth.models import User


class UserMangaHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    follow_updates = models.BooleanField(default=False)
    last_view_date = models.DateTimeField(auto_now=True, null=True)
    last_view_chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.manga.title} - Chapter {self.last_view_chapter}"
