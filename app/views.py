from django.shortcuts import render
from .models import App
import time
from django.http import HttpResponseRedirect
from django.template import Context
from threading import Thread
from calculation.models import Weather
from calculation.models import Calculation
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from _datetime import timedelta
from django.template.context_processors import request
from restaurant.models import Restaurant
import requests
from tkinter.constants import CURRENT
class ProcessThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        

    def run(self):
        currentCR = App.getCR(App)
        now = timezone.now()
        next = now + timedelta(minutes = 5)
        counter = currentCR.periodCounter
        while currentCR.periodCounter > 0 and currentCR.calculationCheck == True:
            weatherCondition = conditionCheck()
            successFlag = Calculation.makePrediction(Calculation, weatherCondition)
            currentCR.countDown()
            time.sleep(1)
        currentCR.calculationCheck = False
        currentCR.save()
def app(request):
    return render(request,'header.html')


def home(request):
    if App.getCR(App) is None:
        return render(request,'home.html')
    else:
        currentCity = App.getCR(App).currentCity
        rules = App.getCR(App)
        flag = rules.calculationCheck
        context = Context({'currentCity': currentCity,'flag':flag})
        return render(request,'home.html',context)

def setCR(request):
    if request.method == 'POST':
        newPeriod = request.POST.get('period',None)
        newCity = request.POST.get('currentCity',None) 
        newApp = App(calculationPeriod = newPeriod,currentCity = newCity,periodCounter = newPeriod,calculationCheck = False)
        newApp.save()
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
       
        return render(request,'setCR.html',context)
    
    else:
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
        return render(request,'setCR.html',context)
    
    
def conditionCheck():
    city = App.getCR(App).currentCity
    getWeather = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ city +'&APPID=b9dd3952f36a165aecc5518e9e0a5117')
    weatherJson = getWeather.json()
    newWeather = weatherJson['weather'][0]['main']
    Weather.setCurrent(Weather, newWeather)
    weatherId = weatherJson['weather'][0]['id']
    if  (weatherId >= 600 and weatherId <=699 ) or (weatherId >= 200 and weatherId <= 299 )  or weatherId >= 900  or ( weatherId >= 501 and weatherId <=599 ) or ( weatherId >= 312 and weatherId <= 321 ) and weatherId == 302 :
        return False
    else:
        return True    
def startApp(request):
    Calculation.setRestCounters(Calculation)
    rules = App.getCR(App)
    rules.calculationCheck = True
    rules.save()
    my_thread = ProcessThread("CacheClassroom")
    my_thread.start()

    return HttpResponseRedirect('calculation/getRecords')


def resetApp(request):
    rules = App.getCR(App)
    rules.calculationCheck = False
    rules.save()
    Calculation.objects.all().delete()
    Restaurant.resetServiceCounters(Restaurant)
    flag = False
    context = Context({'flag':flag})
    return render(request,'home.html',context)