# Generated by Django 4.2.1 on 2023-06-02 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_user_is_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=25, null=True)),
                ('lastname', models.CharField(max_length=25, null=True)),
                ('bio', models.TextField(null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=100)),
                ('profile_pic', models.ImageField(upload_to='profile_pictures/')),
                ('cover_pic', models.ImageField(upload_to='cover_pictures/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
