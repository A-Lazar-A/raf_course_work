# Generated by Django 4.2.7 on 2023-12-12 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_user_avatar_encodings'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_boss',
            field=models.BooleanField(default=False),
        ),
    ]
