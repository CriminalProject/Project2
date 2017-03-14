from django.shortcuts import render
from .models import App
from django.http import HttpResponseRedirect
from django.template import Context
def app(request):
    return render(request,'header.html')


def home(request):
    return render(request,'home.html')

def setCR(request):
    if request.method == 'POST':
        newPeriod = request.POST.get('period',None)
        newCity = request.POST.get('currentCity',None) 
        newApp = App(calculationPeriod = newPeriod,currentCity = newCity,periodCounter = newPeriod,calculationCheck = True)
        newApp.save()
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
        return render(request,'setCR.html',context)
    
    else:
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
        return render(request,'setCR.html',context)
