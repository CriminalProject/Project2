from django.shortcuts import render
from .models import Weather
from django.http import HttpResponseRedirect
from django.template import Context

def setWeather(request):
    if request.method == 'POST':
        newCurrentWeather = request.POST.get('weather',None)
        Weather.setCurrent(Weather,newCurrentWeather)
        currentWt = Weather.getCurrent(Weather)
        context = Context({'Context': currentWt})
        return render(request,'calNweather.html',context)
    
    else:
        currentWt = Weather.getCurrent(Weather)
        context = Context({'Context': currentWt})
        return render(request,'calNweather.html',context)