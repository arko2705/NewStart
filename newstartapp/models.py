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

class Num(models.Model):  ##This tells us about number of companies founds
    companynumber=models.IntegerField(null=True)
class Num1(models.Model):  ##this tells us abt how many companies we want
    limit=models.IntegerField(null=True)
class HeaderList(models.Model):
    Company=models.CharField(max_length=500)
    Address=models.CharField(max_length=500,blank=True)
    PhoneNumber=models.CharField(max_length=500,blank=True)
    MapLink=models.CharField(max_length=500,blank=True)
    Website=models.CharField(blank=True,max_length=500)
    Email=models.CharField(blank=True,max_length=500)
    Linkedin=models.CharField(blank=True,max_length=500) 
class ProcessKeeper(models.Model):
    procID=models.IntegerField(null=True) 

class UserChoice(models.Model):    ##is users take op 1 or op 2.
    choice=models.IntegerField()
class ProcStat(models.Model):
    stat=models.CharField(max_length=50)

class QueryStartStat(models.Model):
    stat=models.CharField(max_length=10)
class QueryStopStat(models.Model):
    stat=models.CharField(max_length=10)



