from django.db import models

# Create your models here.

class Restaurant(models.Model):
    restName = models.CharField(max_length = 50)
    weatherCondition = models.BooleanField()
    modeOfTransport = models.BooleanField()
    serviceStatus = models.BooleanField()
    
    
    def deleteRest(self,delRestName):
        self.objects.get(restName = delRestName).delete()
        self.save()
    def updateRestStatus(self,newStatus,upRestName):
        self.objects.get(restName = upRestName).update(serviceStatus = newStatus)
        self.save()
    def updateRestName(self,upRestName,curRestName):
        self.objects.get(restName = curRestName).update(restName = upRestName)
        self.save()    
    def updateModeOfTransport(self,newMode,upRestName):
        self.objects.get(restName = upRestName).update(modeOfTransport = newMode)
        self.save()
