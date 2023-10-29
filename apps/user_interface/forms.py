from django.forms import ModelForm
from ..manga.models import Manga


class MangaForm(ModelForm):
    class Meta:
        model = Manga
        fields = ["url"]
