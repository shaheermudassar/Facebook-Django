# Generated by Django 4.2.1 on 2023-06-06 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_posts_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general_information',
            name='education',
            field=models.TextField(default='Not Added', null=True),
        ),
        migrations.AlterField(
            model_name='general_information',
            name='hobbies',
            field=models.TextField(default='Not Added', null=True),
        ),
        migrations.AlterField(
            model_name='general_information',
            name='other_interests',
            field=models.TextField(default='Not Added', null=True),
        ),
        migrations.AlterField(
            model_name='general_information',
            name='work_experience',
            field=models.TextField(default='Not Added', null=True),
        ),
    ]
