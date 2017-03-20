from django.db import models
from django.utils import timezone
from grading.models import Points
from restaurant.models import Restaurant
from user.models import User
from app.models import App
import datetime
from random import randint
from django.template.defaultfilters import last
# Create your models here.


class Weather(models.Model):
    currentWeather = models.CharField(max_length = 80)
    date = models.DateField()
    time = models.TimeField()
    
    def getCurrent(self):
        return self.objects.last()
        
    def setCurrent(self, newWeather):
        nowDate = datetime.datetime.now()
        now = timezone.now()
        newWeather = Weather(currentWeather = newWeather,date = nowDate,time = now)
        newWeather.save()
        
class Calculation(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    date = models.DateField()
    
    def getCalculations(self):
        return self.objects.values()
    
    def setRestCounters(self):
        rules = App.getCR(App)
        period = rules.periodCounter
        totalPoints = 0
        for user in User.objects.all():
            totalPoints = period + totalPoints
        
        for rest in Restaurant.objects.filter(serviceStatus = True):
            points = Points.objects.filter(restaurant = rest)
            for point in points:
                serviceCounter = (point.point /totalPoints) * 100 
                intServiceCounter = int(serviceCounter)
                if rest.serviceCounter== 0: 
                    rest.serviceCounter = intServiceCounter
                    rest.save()
            
        
        Restaurant.serviceCounters(Restaurant)    
        rules.save()
        
        
    def makePrediction(self,weatherCondition):
        totalPredictions = Calculation.objects.all().count()
        if weatherCondition == False:
            predictionRestsCount = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True,modeOfTransport = True).count()
            if predictionRestsCount == 0:
                predictionRestsCount = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
                if predictionRestsCount == 0:
                    self.setRestCounters()
                predictionRestsCount = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True,modeOfTransport = True).count()  
                if predictionRestsCount == 0:
                    predictionRestsCount = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
                    if predictionRestsCount == 0:
                        return False
                    
                    predictionRests = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True)
                else:
                    predictionRests = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True,modeOfTransport = True)
            else:
                predictionRests = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True,modeOfTransport = True)
                
            if predictionRestsCount > 1 and totalPredictions >=1:
                last = Calculation.objects.last().restaurant
                for rest in predictionRests:
                    if rest.restName == last.restName:
                        predictionRests.exclude(restName = last.restName)
                        predictionRestsCount = predictionRestsCount -1
                        
            random_index = randint(0, predictionRestsCount - 1)
            nowDate = datetime.datetime.now()  
            predictionRest = predictionRests[random_index]
            predictionRest.serviceCounter = predictionRest.serviceCounter -1
            Calculation(restaurant=predictionRest,date = nowDate)
            return True        
        else:
            predictionRestsCount = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
            if predictionRestsCount == 0:
                self.setRestCounters()
                predictionRestsCount = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
                if predictionRestsCount == 0:
                    return False
                predictionRests = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True)
            else:
                predictionRests = Restaurant.objects.filter(serviceCounter__gt = 0,serviceStatus=True)
            
            onlyPedestrian = False    
            if predictionRestsCount > 1 and totalPredictions >=1:
                last = Calculation.objects.last().restaurant
                for rest in predictionRests:
                    if rest.restName is last.restName:
                        predictionRests.exclude(restName = last.restName)
                        predictionRestsCount = predictionRestsCount -1
                        if last.modeOfTransport == True and predictionRestsCount > 1 and predictionRests.filter(modeOfTransport = False).count()>= 1:
                            onlyPedestrian = True
            if predictionRestsCount > 1 and totalPredictions >= 2:
                last2 = Calculation.objects.all().order_by('-id')[:2]
                for lasts in last2:
                    if lasts.restaurant.modeOfTransport == True and predictionRestsCount > 1 and predictionRests.filter(modeOfTransport = False).count()>= 1:
                        predictionRests.exclude(restName = lasts.restaurant.restName)
                        predictionRestsCount = predictionRestsCount -1
                        onlyPedestrian = True
            
            if onlyPedestrian == True:
                predictionRests = predictionRests.filter(modeOfTransport = False)
            predictionRestsCount = predictionRests.count()
            random_index = randint(0, predictionRestsCount - 1)
            nowDate = datetime.datetime.now()  
            predictionRest = predictionRests[random_index]
            finalRest = Restaurant.objects.get(restName = predictionRest.restName)
            finalRest.serviceCounter = finalRest.serviceCounter -1
            finalRest.save()
            newCalculation = Calculation(restaurant=predictionRest,date = nowDate)
            newCalculation.save()
            return True
                
            
        
    