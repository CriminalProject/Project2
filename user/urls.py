from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'showUsers/', views.showUsers, name='showUsers'),
    url(r'getUser/', views.getUser, name='getUser'),
]
