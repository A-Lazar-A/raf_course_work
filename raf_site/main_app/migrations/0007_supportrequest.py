# Generated by Django 4.2.7 on 2023-12-12 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_remove_department_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_theme', models.CharField(max_length=100)),
                ('about', models.TextField(blank=True, default='', max_length=256)),
                ('is_done', models.BooleanField(default=False)),
                ('request_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
