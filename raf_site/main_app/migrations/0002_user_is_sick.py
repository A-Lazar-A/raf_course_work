# Generated by Django 4.2.7 on 2023-12-09 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_sick',
            field=models.BooleanField(default=False),
        ),
    ]
