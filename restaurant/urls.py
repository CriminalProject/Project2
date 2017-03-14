from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'showRest/', views.showRestaurants, name='showRests'),
    url(r'getRest', views.getRestaurant, name='getRest'),
    url(r'addRest/', views.addRestaurant, name='addRest'),
]
