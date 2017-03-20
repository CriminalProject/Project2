from django.db import models
from app.models import App
import datetime
import math
# Create your models here.

class Restaurant(models.Model):
    restName = models.CharField(max_length = 50)
    weatherCondition = models.BooleanField()
    modeOfTransport = models.BooleanField()
    serviceStatus = models.BooleanField()
    serviceCounter = models.IntegerField()
    
    def deleteRest(self,delRestName):
        self.objects.get(restName = delRestName).delete()
        
    def updateRestStatus(self,newStatus,upRestName):
        rules = App.getCR(App)
        upRestaurant = self.objects.get(restName = upRestName)
        if rules.calculationCheck == True:
            if newStatus == False:
                inactiveRests = self.objects.filter(serviceCounter__gt = 0,serviceStatus=False)
                activeCounter = self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
                for rest in inactiveRests:
                    counter = rest.serviceCunter
                    if activeCounter!= 0:
                        for activeRest in self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).order_by('-serviceCounter'):
                            activeRest.serviceCounter = activeRest.serviceCounter+1
                            counter = counter -1
                            if counter == 0:
                                break
                    else:
                        return False
                            
            else:
                activeRests = self.objects.filter(serviceCounter__gt = 0,serviceStatus=True)
                activeCounter = self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
                for rest in activeRests:
                    counter = rest.serviceCunter
                    if activeCounter!= 0:
                        for activeRest in self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).order_by('-serviceCounter'):
                            if activeRest.serviceCounter != 0:
                                activeRest.serviceCounter = activeRest.serviceCounter-1
                                counter = counter -1
                            if counter == 0:
                                break
                            
                    else:
                        return False
                        
        upRestaurant.serviceStatus = newStatus
        upRestaurant.save()
        return True
        
    def updateRestName(self,upRestName,curRestName):
        upRestaurant = self.objects.get(restName = curRestName)
        upRestaurant.restName = upRestName
        upRestaurant.save()    
        
    def updateModeOfTransport(self,newMode,upRestName):
        upRestaurant = self.objects.get(restName = upRestName)
        upRestaurant.modeOfTransport = newMode
        upRestaurant.save()
        
        
    def updateWeatherCondition(self,newCondition,upRestName):
        upRestaurant = self.objects.get(restName = upRestName)
        upRestaurant.weatherCondition = newCondition
        upRestaurant.save()
    
    def getRestaurants(self):
        return self.objects.values()
    
    def getGrade(self):
        return self.Points
            
    def serviceCounters(self):
        rules = App.getCR(App)
        counter = rules.periodCounter
        for rest in Restaurant.objects.filter(serviceStatus = True):
            counter = counter - rest.serviceCounter
        while counter > 0:
            for rest in Restaurant.objects.filter(serviceStatus = True).order_by('-serviceCounter'):
                rest.serviceCounter = rest.serviceCounter + 1
                rest.save()
                counter = counter -1
                if counter == 0:
                    break
        while counter < 0:
            for rest in Restaurant.objects.filter(serviceStatus = True).order_by('-serviceCounter'):
                rest.serviceCounter = rest.serviceCounter - 1
                rest.save()
                counter = counter +1
                if counter == 0:
                    break
               
        vehicleRestaurants = Restaurant.objects.filter(modeOfTransport = True,serviceStatus = True)
        vrestCounter = 0
        for vrest in vehicleRestaurants:
            vrestCounter = vrest.serviceCounter + vrestCounter
        
        constantIstanbul = [17.5 , 15.3   , 13.8 ,  10.4  , 8.1  , 6.1  ,  4.2  ,  4.9  ,  7.4  , 11.3  ,  13.2  , 17.2]        
        currentDate = datetime.datetime.now()
        currentDay = currentDate.day
        totalDays = rules.periodCounter
        totalMonthsFloat = totalDays/30
        totalMonthsRound = math.ceil(totalMonthsFloat)
        badWeatherProbability = ((30 - currentDay)*constantIstanbul[currentDate.month - 1])/totalDays
        for  i in range(0,totalMonthsRound):
            if (i - totalMonthsFloat) > 0:
                badWeatherProbability = (30*(i - totalMonthsFloat)*constantIstanbul[currentDate.month - 1 + i])/totalDays + badWeatherProbability
            badWeatherProbability = (30*constantIstanbul[currentDate.month - 1 + i])/totalDays + badWeatherProbability      
       
        
        if vrestCounter < int((rules.periodCounter/badWeatherProbability)):
            
            transporBalanceCounter =   int((rules.periodCounter/badWeatherProbability)) - vrestCounter
            counter = transporBalanceCounter
            while transporBalanceCounter > 0:
                for rest in Restaurant.objects.filter(modeOfTransport=False,serviceStatus = True).order_by('-serviceCounter'):
                    rest.serviceCounter = rest.serviceCounter - 1
                    rest.save()
                    counter = counter -1
                    if counter == 0:
                        break
                    
                for rest in Restaurant.objects.filter(modeOfTransport=True,serviceStatus = True).order_by('-serviceCounter'):
                    rest.serviceCounter = rest.serviceCounter + 1
                    rest.save()
                    transporBalanceCounter = transporBalanceCounter -1
                    if transporBalanceCounter == 0:
                        break
                    
                    
    def restaurantBalance(self):
        rests = Restaurant.objects.filter(serviceStatus = True).count()
        vehicleRests = Restaurant.objects.filter(modeOfTransport = True,serviceStatus = True).count()
        if vehicleRests/rests > 0.8:
            return False
        else:
            return True

        
    def resetServiceCounters(self):
        rests = Restaurant.objects.all()
        for rest in rests:
            rest.serviceCounter = 0
            rest.save()
            
            