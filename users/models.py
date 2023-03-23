from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import USER_ROLES
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=125 , blank= True )
    phone_number = models.CharField(max_length=15  , blank=True)
    role = models.CharField(choices=USER_ROLES , default='sales' , max_length=25)
    profile_pic = models.ImageField(upload_to='users/profile_pics' , blank=True , null=True )
    favourite_qouta = models.PositiveIntegerField(default=3)
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    

    @property
    def remaining_qouta(self):
        '''
        Returns the remaining install qouta for the day 
        '''
        today = timezone.now().date()
        used_qouta = self.service_set.filter(service_type = 'install' , favourite = True , created_at__date=today).count()
        remaining = self.favourite_qouta - used_qouta
        
        return remaining