from django.shortcuts import render
from .models import User
from app.models import App
from django.http import HttpResponseRedirect
from django.template import Context
# Create your views here.
def getUser(request):  
    if request.method == 'POST':
        newUserName = request.POST.get('userName',None)
        newUserFirstName = request.POST.get('userFirstName', None)
        newUserLastName = request.POST.get('userLastName', None)
        newUserEmail = request.POST.get('userEmail', None)
        point = App.getCR(App)
        try:
            data = User.objects.get(userName = newUserName)
            return HttpResponseRedirect('user/showUsers/')            
        except User.DoesNotExist:
            newUser = User(userName = newUserName,userFirstName = newUserFirstName , userSurname = newUserLastName, userEmail = newUserEmail)
            newUser.save()
            return HttpResponseRedirect('user/showUsers/')
            
    else:
        return HttpResponseRedirect('user/showUsers/')

    
def showUsers(request):
    users = User.getUsers(User)
    context = Context({'users' : users})
    return render(request,'users.html',context)

def addUser(request):
    return render(request,'AddUser.html')

def updateUser(request):
    return render(request,'updateUser.html')
    