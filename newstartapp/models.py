from django.db import models

# Create your models here.
class GBPInfo(models.Model):
    Company=models.CharField(max_length=500)
    Address=models.CharField(max_length=500)
    PhoneNumber=models.CharField(max_length=500)
    MapLink=models.CharField(max_length=500)
    Website=models.CharField(blank=True,max_length=500)
    Email=models.CharField(blank=True,max_length=500)
    Linkedin=models.CharField(blank=True,max_length=500)
