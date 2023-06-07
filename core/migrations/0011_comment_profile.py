# Generated by Django 4.2.1 on 2023-06-05 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_user_created_at'),
        ('core', '0010_alter_posts_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userauths.profile'),
        ),
    ]
