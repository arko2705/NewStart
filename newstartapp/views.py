from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())
def features(request):
    template=loader.get_template('Features.html')
    return HttpResponse(template.render())
def HTU(request):
    template=loader.get_template('HTU.html')
    return HttpResponse(template.render())
def gs(response):
    template=loader.get_template('BGetStarted.html')
    return HttpResponse(template.render())
def ab(response):
    template=loader.get_template('About.html')
    return HttpResponse(template.render())
def q(response):
    template=loader.get_template('Search1.html')
    return HttpResponse(template.render())
def loading(response):
    template=loader.get_template('loader.html')
    return HttpResponse(template.render())
def data(response):
    template=loader.get_template('display.html')
    return HttpResponse(template.render())




# Create your views here.
