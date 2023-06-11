# Generated by Django 4.2.1 on 2023-06-08 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_user_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0022_alter_general_information_options_friendrequest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='friendrequest',
            name='user',
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='userauths.profile'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='reciever_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieve_friend_requests', to='userauths.profile'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='reciever_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recieve_friend_requests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='sender_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_friend_requests', to='userauths.profile'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='sender_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sent_friend_requests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_friends', to='userauths.profile'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
