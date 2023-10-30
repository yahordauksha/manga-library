from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_project.settings")

app = Celery("manga_project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.broker_url = "redis://local_host:6379/0"
