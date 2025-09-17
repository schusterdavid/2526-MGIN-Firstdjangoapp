from django.db import models

# Create your models here.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateTimeField()
    svnr = models.CharField(max_length=11)
