from django.db import models
from django.utils import timezone
from restaurant.models import Restaurant
import datetime
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
    
    def makePrediction(self,weather):
        if weather == 'Rain' or weather == 'Snow' or weather == 'aShower':
            preRest = Restaurant.objects.filter(modeOfTransport = True , serviceStatus = True )
    