# Generated by Django 4.2.5 on 2023-10-05 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0011_manga_first_chapter_manga_last_chapter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='number',
        ),
    ]