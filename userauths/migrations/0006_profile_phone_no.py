# Generated by Django 4.2.1 on 2023-06-03 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0005_profile_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_no',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
