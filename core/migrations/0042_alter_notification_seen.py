# Generated by Django 4.2.1 on 2023-06-13 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_notification_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
