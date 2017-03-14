from django.shortcuts import render
from .models import Restaurant
from django.http import HttpResponseRedirect
from django.template import Context
# Create your views here.
def getRestaurant(request):  
    if request.method == 'POST':
        newRestName = request.POST.get('restName',None)
        newWeatherCondition = request.POST.get('weatherCondition', None)
        newModeOfTransport = request.POST.get('modeOfTransport', None)
        
        try:
            data = restaurant.objects.get(restName = newRestName)
            return HttpResponseRedirect('restaurant/showRest/')            
        except User.DoesNotExist:
            newRest = Restaurant(restName = newRestName,weatherCondition = newWeatherCondition , modeOfTransport = newModeOfTransport)
            newRest.save()
            return HttpResponseRedirect('restaurant/showRest/')
        
        
    
    else:
        return HttpResponseRedirect('restaurant/showRest/')

def showRestaurants(request):
    restaurants = Restaurant.getRestaurants(Restaurant)
    context = Context({'restaurants' : restaurants})
    return render(request,'restaurants.html',context)
    
    
def addRestaurant(request):
    return render('addRestaurant.html')
    
    