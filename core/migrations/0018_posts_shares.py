# Generated by Django 4.2.1 on 2023-06-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_general_information_education_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='shares',
            field=models.IntegerField(default=0, null=True),
        ),
    ]