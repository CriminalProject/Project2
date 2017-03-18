from django.shortcuts import render
from .models import App
import time
from django.http import HttpResponseRedirect
from django.template import Context
from threading import Thread
from calculation.models import Weather
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from _datetime import timedelta
from django.template.context_processors import request


class ProcessThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        

    def run(self):
        currentCR = App.getCR(App)
        now = timezone.now()
        next = now + timedelta(minutes = 5)
        while next >= now:
            time.sleep(10)
            now = timezone.now()
            currentCR.countDown()

def app(request):
    return render(request,'header.html')


def home(request):
    if App.getCR(App) is None:
        return render(request,'home.html')
    else:
        currentCity = App.getCR(App).currentCity
        context = Context({'currentCity': currentCity})
        return render(request,'home.html',context)

def setCR(request):
    if request.method == 'POST':
        newPeriod = request.POST.get('period',None)
        newCity = request.POST.get('currentCity',None) 
        newApp = App(calculationPeriod = newPeriod,currentCity = newCity,periodCounter = newPeriod,calculationCheck = True)
        newApp.save()
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
       
        return render(request,'setCR.html',context)
    
    else:
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
        return render(request,'setCR.html',context)
    
    

def startApp(request):
    my_thread = ProcessThread("CacheClassroom")
    my_thread.start()
    return HttpResponseRedirect('setCR')