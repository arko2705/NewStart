from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from background_task import background
from CodeLogic import anothermain2
from CodeLogic import anothermain1
from django.db import models
from .models import GBPInfo
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
    outcome="done"
    return outcome

def q(request):
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
            'option':choice
        }
    return HttpResponse(template.render(context))

def loading(request):
    template=loader.get_template('loader.html')
    GBPInfo.objects.all().delete()
    if choice=='OP-1' and status !="starting":
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
    context={
        'headers':['Company','Address','Phone Number','Map-Link','Website','E-Mail','Linkedin'],
        'values':values,
        'outcome':outcome
    }

    return HttpResponse(template.render(context,request))


    




# Create your views here.
