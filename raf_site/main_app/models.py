import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # full_name = models.CharField(max_length=100)
    # document_id = models.CharField(max_length=10, unique=True)
    # pernr = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=100)
    # boss = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True)
    # is_boss = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    user_phone_num = models.CharField(max_length=15, null=True, blank=True)
    # avatar = models.ImageField(upload_to=path_and_rename, default='default_avatar.svg')
    at_workplace = models.BooleanField(default=False)
    # avatar_encodings = models.JSONField(default=dict)
    about = models.TextField(max_length=256, blank=True, default='')
    work_time_30days = models.FloatField(default=0)
    work_time_7days = models.FloatField(default=0)
    work_time_1days = models.FloatField(default=0)
    is_on_holiday = models.BooleanField(default=False)
    is_sick = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-updated', '-username']

    def __str__(self):
        return str(self.username)


class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    department_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100)
    max_users = models.PositiveIntegerField(default=0)
    staff = models.JSONField(null=True)

    def __str__(self):
        return str(self.department_name)
# Create your models here.
