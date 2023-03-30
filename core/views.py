from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from . import models
from .forms import CustomerForm
from .filters import CustomerFilter
from service.models import Service , SparePartRequest, Appointment
from django.db.models import Count, Q



class Index(generic.View):
    def get(self, request):
        template = ''
        ctx = {}

        if request.user.role == 'admin' or request.user.is_superuser:
            counts = Service.objects.aggregate(
                total_counts=Count('id'),

                repair_count=Count('id', filter=Q(service_type='repair')),
                repair_new_count=Count('id', filter=Q(
                    service_type='repair', status='new')),
                install_count=Count('id', filter=Q(service_type='install')),
                install_new_count=Count('id', filter=Q(
                    service_type='install', status='new')),
                new_count=Count('id', filter=Q(status='new')),
                under_process_count=Count(
                    'id', filter=Q(status='under_process')),
                on_hold_count=Count('id', filter=Q(hold=True))
            )
            new_requests = Service.objects.all().filter(status = 'new')
            template = 'core/index.html'
            ctx = {
                'total_count': counts['total_counts'],
                'repair_count': counts['repair_count'],
                'repair_new_count': counts['repair_new_count'],
                'install_count': counts['install_count'],
                'install_new_count': counts['install_new_count'],
                'new_count': counts['new_count'],
                'under_process_count': counts['under_process_count'],
                'on_hold_count': counts['on_hold_count'],
                'new_requests' : new_requests
                
            }
        elif request.user.role == 'sales':
            template = 'core/sales_index.html'
            counts = Service.objects.filter(created_by=request.user).aggregate(
                total_count=Count('id'),
                repair_count=Count('id', filter=Q(service_type='repair')),
                repair_new_count=Count('id', filter=Q(
                    service_type='repair', status='new')),
                install_count=Count('id', filter=Q(service_type='install')),
                install_new_count=Count('id', filter=Q(
                    service_type='install', status='new')),
                new_count=Count('id', filter=Q(status='new')),
                under_process_count=Count(
                    'id', filter=Q(status='under_process')),
                on_hold_count=Count('id', filter=Q(status='hold'))

            )
            ctx = {
                'total_count': counts['total_count'],
                'repair_count': counts['repair_count'],
                'repair_new_count': counts['repair_new_count'],
                'install_count': counts['install_count'],
                'install_new_count': counts['install_new_count'],
                'new_count': counts['new_count'],
                'under_process_count': counts['under_process_count'],
                'on_hold_count': counts['on_hold_count'],
                'services': Service.objects.filter(created_by=request.user)
            }
        elif request.user.role == 'company':
            template = 'core/company_index.html'
            ctx = {
                'services': Service.objects.filter(created_by=request.user),
                'warranty': Service.objects.repair().filter(company=request.user),
                'sp_requests': SparePartRequest.objects.all().filter(service__company = request.user )
            }
        elif request.user.role == 'technician':
            template = 'core/tech_index.html'
            ctx = {
                'upcoming_appointments' : Appointment.objects.upcoming().filter(technician=request.user) , 
                'past_appointmanets' :Appointment.objects.past().filter(technician = request.user ) , 
                'services'  :Service.objects.all().filter(created_by = request.user )
            }
        elif request.user.role == 'repair_supervisor':
            return (redirect(reverse_lazy('service:repair')))
        elif request.user.role == 'install_supervisor':
            return (redirect(reverse_lazy('service:install')))
        return render(request, template, ctx)


class CustomerList(generic.ListView):
    model = models.Customer
    template_name = 'core/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        print(self.request.GET)
        qs = super().get_queryset()
        if self.request.user.role == 'sales':
            qs = self.model.objects.filter(created_by=self.request.user)
        self.filterset = CustomerFilter(self.request.GET, queryset=qs)
        return self.filterset.qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        kwargs['customer_form'] = CustomerForm
        kwargs['filterform'] = self.filterset.form
        return super().get_context_data(**kwargs)


class CreateCustomerView(generic.CreateView):
    model = models.Customer
    fields = ['name', 'phone_number', 'address', 'city']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'تم اضافة العميل !')
        return redirect(self.request.META.get('HTTP_REFERER'))


class CustomerDetails(generic.DetailView):
    model = models.Customer
    lookup_field = 'pk'
    context_object_name = 'customer'
    template_name = 'core/customer_details.html'

class Archive(generic.ListView):
    
    '''
    List all aarchived services 
    service is archived after 30 days if status == closed
    '''
    template_name = 'service/archive.html'
    model = Service
    context_object_name = 'services'
    
    def get_queryset(self):
        if self.request.user.is_superuser :
            qs = Service.objects.archive() 
        elif self.request.user.role == 'install_supervisor' : 
            qs =Service.objects.archive().filter(service_type = 'install')
        elif self.request.user.role == 'repair_supervisor' : 
            qs =Service.objects.archive().filter(service_type = 'repair')
        else :
            qs = self.request.user.service_set.filter(archive = True )
        print(qs.explain())
        return qs

# dashboard htmx 
def index_data(request):
    '''
    Htmx tables in index page 
    repair == new , current 
    install == new , current 
    hold  
    '''
    service_type = request.GET['service']
    base_temp_name = 'core/partials/htmx/'
    if service_type == 'install' :
        template = base_temp_name + 'install.html'
        ctx = {
            'services' : Service.objects.install().filter(Q(status = 'new') | Q(status = 'under_process'))
        }
    elif service_type == 'repair':
        template = base_temp_name + 'repair.html'
        ctx = {
            'services' : Service.objects.repair().filter(Q(status = 'new') | Q(status = 'under_process'))
        }
    elif service_type == 'hold':
        template = base_temp_name + 'hold.html'
        ctx = {
            'services' : Service.objects.repair().filter(hold=True)
        }
        
    return render(request , template , ctx )

def empty_htmx(request):
    return render(request , 'core/empty_htmx.html')