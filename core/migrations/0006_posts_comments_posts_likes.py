# Generated by Django 4.2.1 on 2023-06-04 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_posts_content_general_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='comments',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
