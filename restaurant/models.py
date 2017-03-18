from django.db import models
from django.db.models.fields import IntegerField
# Create your models here.

class Restaurant(models.Model):
    restName = models.CharField(max_length = 50)
    weatherCondition = models.BooleanField()
    modeOfTransport = models.BooleanField()
    serviceStatus = models.BooleanField()
    serviceCounter = IntegerField()
    
    def deleteRest(self,delRestName):
        self.objects.get(restName = delRestName).delete()
        
    def updateRestStatus(self,newStatus,upRestName):
        upRestaurant = self.objects.get(restName = upRestName)
        upRestaurant.serviceStatus = newStatus
        upRestaurant.save()
        
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
            
        