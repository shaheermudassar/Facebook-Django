# Generated by Django 4.2.1 on 2023-06-07 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_user_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0018_posts_shares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SharedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('original_post_id', models.IntegerField(null=True, unique=True)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userauths.profile')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Shared_Posts',
            },
        ),
        migrations.AddField(
            model_name='posts',
            name='shared_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.sharedpost'),
        ),
    ]
