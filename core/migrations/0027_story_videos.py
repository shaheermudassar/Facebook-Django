# Generated by Django 4.2.1 on 2023-06-09 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_remove_story_videos_alter_story_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='videos',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]