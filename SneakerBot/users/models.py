from django.db import models
from django.contrib.auth.models import User

MAX_ACCOUNTS = 100
# Create your models here.
class NikeTestBackEnd(models.Model):
    url = models.CharField(max_length=120, default=None)
    size = models.CharField(max_length=8, default=None)
    username = models.CharField(max_length=60, default=None)
    password = models.CharField(max_length=60, default=None)

    def __str__(self):
        return f'Nike Profile'

class WebProfile(models.Model):
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    #text_profiles = models.FileField(default='null.txt', upload_to='profile_pics')

    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.username}\'s WebSite-Profiles' 
        
    def create(self):
        username = self.username
        password = self.password
        
            
    #Need to create "profile" for Address format for database entries to go with user thats logged in;

