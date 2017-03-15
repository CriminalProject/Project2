from django.db import models
from user.models import User
from restaurant.models import Restaurant
# Create your models here.
class Points(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    point = models.IntegerField()
    
    def newPoint(self,User,Restaurant,inPoint):
        newPoint = Points(user = User,restaurant = Restaurant,point =inPoint)
        newPoint.save()