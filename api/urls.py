from django.urls import path
from . import views 


app_name = 'api'
urlpatterns = [
    path('customers' , views.CustomerList.as_view() , name='customer_list')    
]
