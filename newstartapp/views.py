from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from CodeLogic import bgtasks
from django.db import models
from .models import GBPInfo,Num,Num1,HeaderList,ProcStat,UserChoice,QueryStartStat
from celery import current_app
from newstartapp.tasks import start1,start2
def index(request):
    bgtasks.deletingBG()
    QueryStartStat(stat="STOPPED").save()  ##For someone who just quits midway,thus whenever homepage opened again previous task will be deleted and stat will be stopped/
    for i in [UserChoice,ProcStat]:  ##this stores '0' indicating that process ended midway,but for a fresh start is getting deleted again.
      i.objects.all().delete()     ## ProcStat deletes user choice
    return HttpResponse(loader.get_template('index.html').render())
def features(request):
    return HttpResponse(loader.get_template('Features.html').render())
def HTU(request):
    return HttpResponse(loader.get_template('HTU.html').render())
def gs(request):
    return HttpResponse(loader.get_template('BGetStarted.html').render())
def ab(request):
    return HttpResponse(loader.get_template('About.html').render())


def q(request):
 current_app.control.purge()
 try:
    for i in [Num1,ProcStat]:
        i.objects.all().delete()
    choice=request.GET.get("User_Choice")
    context={
            'option':choice
        }
    if choice=="OP-1":
        ProcStat(stat=1).save()   #saving user choices,yeah renamed the model badly.sorry abt that
    elif choice=="OP-2":
        ProcStat(stat=2).save()
    return HttpResponse(loader.get_template('Search1.html').render(context)) 
 except:
    return HttpResponse(loader.get_template('Error.html').render())

def loading(request):
  if QueryStartStat.objects.last() and QueryStartStat.objects.last().stat=="STARTED":
       QueryStartStat.objects.all().delete()
       QueryStartStat(stat="STOP IT").save()
       return HttpResponse(loader.get_template('dontspam.html').render())
  try:
    for i in [GBPInfo,Num,Num1]:
       i.objects.all().delete() 
    quer=request.GET.get('loading')  
    if ProcStat.objects.last().stat=='1':         
        start1.delay(quer)                 ##a is the query being passed
        
    elif ProcStat.objects.last().stat=='2':
        user_choices=request.GET.getlist('fields')
        print(user_choices)
        start2.delay(quer,user_choices)  

    return HttpResponse(loader.get_template('loader.html').render())

  except:
    return HttpResponse(loader.get_template('Error.html').render())

def datadisplay(request):
    values=GBPInfo.objects.all().values()
    limit=request.GET.get("number-input")   ##takes how many inputs users want,from the number page.The number.html sends data to datadisplay
    Num1(limit=limit).save()

    try: 
     if GBPInfo.objects.last():
        last_stat=GBPInfo.objects.last().Stat
        if ProcStat.objects.last().stat=='1':
           keys=['Company','Address','Phone Number','Map-Link','Website','E-Mail','Linkedin']
        elif ProcStat.objects.last().stat=='2':
           headers=HeaderList.objects.last()     
           keys=[headers.Company,headers.Address,headers.PhoneNumber,headers.MapLink,headers.Website,headers.Email,headers.Linkedin]
        context={
              'values':values,
              'last_stat':last_stat,
              'keys':keys
           }
           
     else:
         last_stat="nun"    ###this is only to cover up on the part where my page directly goes to Your data,and no first column has been rendered yet.There,there exists no GBPInfo.objects.last(),hence theres an error.But i dont want an error,i just want that the data has not been loaded yet,which is being handled through conditional statements on the same page.Hence all the trouble
         context={
        'last_stat':last_stat,
        } 
     return HttpResponse(loader.get_template('display.html').render(context,request))
          
    except :
        return HttpResponse(loader.get_template('Error.html').render())


def num(request):
    if UserChoice.objects.last() and UserChoice.objects.last().choice==0:        ##0 indicates they took too long to respond
        return HttpResponse(loader.get_template("toolong.html").render())
    
    if Num.objects.last() is not None:  
        context={
            's':"yes",                        ##indicating that we found the number of companies
            'num':Num.objects.last().companynumber        ##model values have to be sent in context,cant be directly accessed by html pages.
        }
    else:
     context={
        's': "no"
     }
    return HttpResponse(loader.get_template("number.html").render(context))



   
   
    




# Create your views here.
