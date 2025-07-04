from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from background_task import background
from CodeLogic import anothermain2
from CodeLogic import anothermain1
from django.db import models
from .models import GBPInfo,Num
from CodeLogic import bgtasks
outcome=None 
status=None
def index(request):
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
def start1(a):
    status="starting"
    print("starting 1st process")
    element_list=anothermain2.main(a)
    print("sort")
    return 

@background()
def start2(a):
    print("starting 2nd process")
    anothermain1.main(a)
    return

def q(request):
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

def loading(request):

    template=loader.get_template('loader.html')
    if choice=='OP-1' and status !="starting":##to ensure that no fuckery's been done when the user goes out but comes back to te loading page again.
        GBPInfo.objects.all().delete()
        a=request.GET.get('loading')
        start1(a,repeat=None)
        
    elif choice=='OP-2':
        a=request.GET.get('loading')
        start2(a,repeat=None)
    
    else:
        pass
    return HttpResponse(template.render())

def datadisplay(request):
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
        return HttpResponse(template.render())

def num():
    
    template=loader.get_template("number.html")
    no=Num.objects.last().companynumber
    context={
        'num':no
    }
    return HttpResponse(template.render(context))



    




# Create your views here.
