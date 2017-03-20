from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^weather$', views.setWeather, name='setWeather'),
url(r'^getRecords$', views.serviceRecord, name='getRecords'),
]