from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    SECURITY_QUESTIONS = (
        (1, 'What is your mother\'s maiden name?'),
        (2, 'What city were you born in?'),
        (3, 'What is your  high school mascot?'),
        (4, 'What is the name of your first pet?'),
        (5, 'In what city was your high school?'),
    )
    user = models.ForeignKey(User, unique=True)
    sQuestion = models.IntegerField(max_length=1, choices=SECURITY_QUESTIONS);
    sAnswer = models.CharField(max_length=50)
    lastAddress = models.IPAddressField()
    
class Alarm(models.Model):
    creator = models.CharField(max_length=18) #Creators Username
    buildingID = models.ForeignKey('Building') #Foreign Key
    outletID = models.ForeignKey('Outlet') #Foreign Key
    alarmName = models.CharField(max_length=25)
    startTime = models.DateTimeField(blank = True, null = True)
    endTime = models.DateTimeField()
    desiredState = models.NullBooleanField(blank = True, null = True)
    #For a timer startTime is NULL and endTime will be used to calculate the duration
    
    def __unicode__(self):
        return self.alarmName
    
class Building(models.Model):
    buildingname = models.CharField(max_length=18)
    owner = models.ForeignKey(User) #Foreign Key
    onlineState = models.BooleanField()
    
    def __unicode__(self):
        return self.buildingname
    
class Outlet(models.Model):
    outletName = models.CharField(max_length=25)
    buildingID = models.ForeignKey('Building') #Foriegn Key
    state = models.BooleanField()
    energyTotal = models.IntegerField()
    
    def __unicode__(self):
        return self.outletName
