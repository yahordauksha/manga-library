from celery.schedules import crontab
from ..apps.scraper.scrapers.updates import get_updates
from .settings import app

app.conf.beat_schedule = {
    "get_updates": {
        "task": "..apps.scraper.scrapers.updates.get_updates",
        "schedule": crontab(minute="*/1"),  # Run every 1 minute
    },
}


# celery -A manga_project worker -l debug
# celery -A manga_project beat -l debug
