# Generated by Django 4.2.1 on 2023-06-02 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_post_posts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name_plural': 'Posts'},
        ),
    ]
