from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.app, name='app'),
    url(r'^home/$', views.home),
    url(r'setCR/^$', views.setCR, name='setcr'),
]
