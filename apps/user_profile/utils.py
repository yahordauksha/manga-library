from .models import UserMangaHistory
from ..manga.models import Chapter
import pdb


def update_last_viewed_chapter(user, manga, current_chapter):
    # pdb.set_trace()
    try:
        history = UserMangaHistory.objects.get(user=user, manga=manga)
    except UserMangaHistory.DoesNotExist:
        # If no history exists, create a new one with last_view_chapter=None
        history = UserMangaHistory(user=user, manga=manga)
        print("Created manga history!")

    if current_chapter:
        if current_chapter.id is not None and (
            history.last_view_chapter is None
            or current_chapter.id > history.last_view_chapter.id
        ):
            # Update the history if the current chapter is newer
            history.last_view_chapter = current_chapter
            history.save()
            print("Last viewed chapter was successfully updated.")
    else:
        history.save()

    return history
