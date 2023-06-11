# Generated by Django 4.2.1 on 2023-06-09 15:24

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_remove_story_sid'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='sid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=30, null=True, prefix='stry', unique=True),
        ),
    ]