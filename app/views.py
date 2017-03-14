from django.shortcuts import render

def app(request):
    return render(request,'header.html')


def home(request):
    return render(request,'home.html')

def setCR(request):
    return render(request,'setCR.html')