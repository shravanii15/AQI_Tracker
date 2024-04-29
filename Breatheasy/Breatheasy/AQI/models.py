from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image  = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    type = models.CharField(max_length=15,null=True)
    def _str_(self):
        return self.user.username

class Location(models.Model):
    place = models.CharField(max_length=255)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField()
    pm25 = models.FloatField(null=True, blank=True)
    pm10 = models.FloatField(null=True, blank=True)
    o3 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)
    so2 = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='location_images', null=True, blank=True)

    
    # Other fields...
