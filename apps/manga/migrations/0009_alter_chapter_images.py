# Generated by Django 4.2.5 on 2023-09-23 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0008_alter_chapter_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='images',
            field=models.JSONField(blank=True, null=True),
        ),
    ]