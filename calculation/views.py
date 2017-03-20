from django.shortcuts import render
from .models import Weather
from .models import Calculation
from django.http import HttpResponseRedirect
from django.template import Context
from restaurant.models import Restaurant

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
        
    
    
    
def serviceRecord(request):
    row = []
    returnList = []
    counter = 1
    for record in Calculation.objects.all():
                rest = Restaurant.objects.get(restName = record.restaurant.restName ) 
                row = {'counter':counter,'restaurant':rest.restName,'date':record.date,'modeOfTransport':rest.modeOfTransport}
                counter = counter+1
                returnList.append(row)
    context = Context({'Records' : returnList})
    return render(request,'records.html',context)
    
    