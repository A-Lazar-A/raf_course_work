# Generated by Django 4.2.7 on 2023-12-10 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_user_options_remove_user_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar_encodings',
        ),
    ]