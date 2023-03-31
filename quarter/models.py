from django.db import models
from users.models import User
from .choices import PORJECT_STATUS_CHOICES , NEGOTIATION_STATUS_CHOICES
from datetime import datetime
from django.db.models import Max
# Create your models here.

def generate_ref_number():
    prefix = 'Q'
    year = str(datetime.now().year)[-2:]

    last_ref_number =   QuarterProject.objects.filter(
        ref_number__startswith=f'{prefix}{year}'
    ).aggregate(Max('ref_number'))['ref_number__max']

    if not last_ref_number:
        return f'{prefix}{year}001'

    last_number = int(last_ref_number[-3:])
    new_number = f'{last_number+1:03d}'
    return f'{prefix}{year}{new_number}'



class QuarterProject(models.Model):
    ref_number = models.CharField(max_length=12 , default=generate_ref_number, unique=True)
    name = models.CharField(max_length=255 )
    phone_number = models.CharField(max_length=15)
    address =models.CharField(max_length=255 , blank=True , null = True )
    status = models.CharField(max_length=20 , default='new' , choices = PORJECT_STATUS_CHOICES)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , null = True )
    created_at = models.DateTimeField(auto_now_add=True )
    last_update = models.DateTimeField(auto_now=True )
    

    def __str__(self) :
        return self.ref_number
    
class Negotiation(models.Model):
    project = models.ForeignKey(QuarterProject , on_delete=models.CASCADE)
    created_by = models.ForeignKey(User ,on_delete=models.SET_NULL , null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10 , choices=NEGOTIATION_STATUS_CHOICES , default='current')
    
    