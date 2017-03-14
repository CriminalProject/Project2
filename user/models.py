from django.db import models

# Create your modeclls here.
class User(models.Model):
    userName = models.CharField(max_length= 40)
    userSurname = models.CharField(max_length= 40)
    userFirstName = models.CharField(max_length= 40)
    userEmail = models.EmailField()
    userPoints = models.IntegerField()
    
    
    
    def updateUser(self,User):
        self.userName = User.userName
        self.userSurname = User.userSurname
        self.userFirstName = User.userFirstName
        self.userEmail = User.userEmail
        self.save()
        
    
    def deleteUser(self,delUser):
        self.objects.get(userName = delUser).delete()
        self.save()
        
    def getUsers(self):
        return self.objects.values()