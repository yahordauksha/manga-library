# Generated by Django 4.2.5 on 2023-09-25 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0009_alter_chapter_images'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermangahistory',
            name='last_view_chapter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manga.chapter'),
        ),
    ]