# Generated by Django 5.1.4 on 2025-01-17 04:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='grupos_permitidos',
            field=models.ManyToManyField(blank=True, related_name='classes', to='auth.group'),
        ),
        migrations.AddField(
            model_name='classe',
            name='publico',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='classe',
            name='usuarios_permitidos',
            field=models.ManyToManyField(blank=True, related_name='classes', to=settings.AUTH_USER_MODEL),
        ),
    ]
