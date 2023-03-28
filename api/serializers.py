from core.models import Customer
from rest_framework import serializers 
from service.models import SparePartRequest

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = '__all__'
        
class SparePartRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePartRequest
        fields = '__all__'