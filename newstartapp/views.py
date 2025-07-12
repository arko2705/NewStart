from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from background_task import background
from CodeLogic import anothermain2
from CodeLogic import anothermain1
from django.db import models
from .models import GBPInfo,Num,Num1
from CodeLogic import bgtasks
status=None
def index(request):
    bgtasks.deletingBG()           ##deletes all background tasks everytime someone comes to the frontpage,taking care of the error page's go back to home and restart process button.
    template=loader.get_template('index.html')
    return HttpResponse(template.render())
def features(request):
    template=loader.get_template('Features.html')
    return HttpResponse(template.render())
def HTU(request):
    template=loader.get_template('HTU.html')
    return HttpResponse(template.render())
def gs(request):
    template=loader.get_template('BGetStarted.html')
    return HttpResponse(template.render())
def ab(request):
    template=loader.get_template('About.html')
    return HttpResponse(template.render())
@background()
def start1(quer):
    status="starting"
    print("starting 1st process")
    anothermain2.main(quer)     ##a is the query being passed
    return
@background()
def start2(quer,user_choices):
    status="starting"
    print("starting 2nd process")
    anothermain1.main(quer,user_choices)
    return

def q(request):
 try:
    Num1.objects.all().delete()
    bgtasks.deletingBG()##so as to ensure everytiume someone comes to search something the previous tasks go away.
    template=loader.get_template('Search1.html')
    global choice
    context=None
    choice=request.GET.get("User_Choice")
    
    if choice=="OP-1":
        context={
            'option':choice
        }
    elif choice=="OP-2":
        context={
            'option':choice,
        }
    return HttpResponse(template.render(context)) 
 except:
    template=loader.get_template('Error.html')
    return HttpResponse(template.render())

def loading(request):
 try:
    template=loader.get_template('loader.html')
    if choice=='OP-1' and status !="starting":##to ensure that no fuckery's been done when the user goes out but comes back to te loading page again.
        GBPInfo.objects.all().delete()       ###This is present only here,so that data gets deleted only when a person searches something else again.Else they might go back to some page and would want to come to datadisplay page again.
        Num.objects.all().delete()
        a=request.GET.get('loading')          ##a is the query being passed
        start1(a,repeat=None)
        
    elif choice=='OP-2' and status !="starting":
        GBPInfo.objects.all().delete()
        quer=request.GET.get('loading')
        user_choices=request.GET.getlist('fields')
        start2(quer,user_choices,repeat=None)   ##repeat=None--->It means the background process will run only once, unless something else restarts it.


    
    else:
        pass
    return HttpResponse(template.render())

 except:
    template=loader.get_template('Error.html')
    return HttpResponse(template.render())

'''def datadisplay(request):
    template=loader.get_template('display.html')
    values=GBPInfo.objects.all().values()
    try:
      if GBPInfo.objects.last().Stat=="done":
         context={
        'headers':['Company','Address','Phone Number','Map-Link','Website','E-Mail','Linkedin'],
        'values':values,
        } 
         return HttpResponse(template.render(context,request))
      else:
         template=loader.get_template('Error.html')
         return HttpResponse(template.render())
          
     
    except:
        template=loader.get_template('Error.html')
        return HttpResponse(template.render())'''
def datadisplay(request):
    template=loader.get_template('display.html')
    values=GBPInfo.objects.all().values()
    limit=request.GET.get("number-input")   ##takes how many inputs users want,from the number page.The number.html sends data to datadisplay
    Num1(limit=limit).save()

    try:
      if GBPInfo.objects.last():
        last_stat=GBPInfo.objects.last().Stat
        context={
        'headers':['Company','Address','Phone Number','Map-Link','Website','E-Mail','Linkedin'],
        'values':values,
        'last_stat':last_stat,
        } 
      else:
         last_stat="nun"    ###this is only to cover up on the part where my page directly goes to Yourdata,and no first column has been rendered yet.There,there exists no GBPInfo.objects.last(),hence theres an error.But i dont want an error,i just want that the data has not been loaded yet,which is being handled through conditional statements on the same page.Hence all the trouble
         context={
        'last_stat':last_stat,
        } 
      return HttpResponse(template.render(context,request))
          
     
    except:
        template=loader.get_template('Error.html')
        return HttpResponse(template.render())


def num(request):
    template=loader.get_template("number.html")
    if Num.objects.last() is not None:
        s="yes"   ##indicating that we found the number of companies
        context={
            's':"yes",
            'num':Num.objects.last().companynumber
        }
    else:
    
     context={
        's': "no"
     }
    return HttpResponse(template.render(context))



    




# Create your views here.
