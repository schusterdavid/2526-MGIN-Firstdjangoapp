from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
# Create your models here.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_birth = models.DateTimeField()
    svnr = models.CharField(max_length=11)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class practitioner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    specilization = models.CharField(max_length=32)