from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from background_task import background
from CodeLogic import anothermain2
from CodeLogic import anothermain1
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
    print("starting 1st process")
    anothermain2.main(a)
    print("sort")
    return
@background()
def start2(a):
    print("starting 2nd process")
    anothermain1.main(a)
    print("sort")
    return

def q(request):
    template=loader.get_template('Search1.html')
    global choice
    choice=request.GET.get("User_Choice")
    return HttpResponse(template.render())

def loading(request):
    template=loader.get_template('loader.html')
    if choice=='OP-1':
        a=request.GET.get('loading')
        start1(a,repeat=None)

    elif choice=='OP-2':
        a=request.GET.get('loading')
        start2(a,repeat=None)
    
    else:
        pass
    return HttpResponse(template.render())

def data(request):
    template=loader.get_template('display.html')
    return HttpResponse(template.render())


    




# Create your views here.
