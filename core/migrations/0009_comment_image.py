# Generated by Django 4.2.1 on 2023-06-05 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
