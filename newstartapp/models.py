from django.db import models

# Create your models here.
class GBPInfo(models.Model):  ##to display
    Company=models.CharField(max_length=500)
    Address=models.CharField(max_length=500,blank=True)
    PhoneNumber=models.CharField(max_length=500,blank=True)
    MapLink=models.CharField(max_length=500,blank=True)
    Website=models.CharField(blank=True,max_length=500)
    Email=models.CharField(blank=True,max_length=500)
    Linkedin=models.CharField(blank=True,max_length=500)
    Stat=models.CharField(max_length=5,blank=True)

class TaskStatus(models.Model):  ##needs to be deleted,as Stat in GBPInfo already takes care of it
    stat=models.CharField(max_length=10,default='rest')
class Num(models.Model):  ##This tells us about number of companies founds
    companynumber=models.IntegerField(null=True)
class Num1(models.Model):  ##this tells us abt how many companies we want
    limit=models.IntegerField(null=True)
class HeaderList(models.Model):
    Company=models.CharField(max_length=500)
    

