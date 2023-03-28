from . import views
from django.urls import path


app_name = 'core'
urlpatterns = [
    path('' , views.Index.as_view() ,name='index'),
    path('customers' , views.CustomerList.as_view() , name='customer_list'),
    path('customers/new' , views.CreateCustomerView.as_view() , name='add_customer'),
    path('customers/<int:pk>/details' , views.CustomerDetails.as_view() , name='customer_details'),
    path('archive' , views.Archive.as_view() , name='archive')
]
