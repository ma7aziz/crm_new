from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.views import generic
from . import models 
from .forms import QuarterProjectForm
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.

##list view 
class ProjectList(generic.ListView):
    model = models.QuarterProject
    template_name = 'quarter/project_list.html'
    context_object_name = 'projects'
    
    
class CreateProject(generic.CreateView):
    model = models.QuarterProject
    form_class = QuarterProjectForm
    success_url = reverse_lazy('quarter:project_list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request , 'تم اضافة الطلب !')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request , 'خطأ يرجي المحاولة مرة اخري ')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

class UpdateProject(generic.UpdateView):
    model = models.QuarterProject
    form_class = QuarterProjectForm
    
    def form_valid(self,form):
        messages.success(self.request , 'تم التحديث !')
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('quarter:project_details' , kwargs ={'pk': self.object.pk})

class DeleteProject(generic.DeleteView):
    model = models.QuarterProject
    success_url  = reverse_lazy('quarter:project_list')
    
    def delete(self, request , *args ,  **kwargs) :
        messages.warning(request , 'تم حذف المشروع !!')
        return super().delete(request, *args, **kwargs)

class ProjectDetails(generic.DetailView):
    model = models.QuarterProject
    context_object_name = 'project'
    template_name = 'quarter/project_details.html'
    lookup_field = 'id'
    

# start negotiaion 
class StartNegotiation(generic.View):
    def post(self ,request ):
        project = models.QuarterProject.objects.get(pk = request.POST['project'])
        negotiation = models.Negotiation(
            project = project,
            created_by = request.user
        )
        negotiation.save()
        project.status = 'negotiation'
        project.save()
        messages.success(request , 'بدأ المفاوضات  !!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
class NegotiationStatus(generic.View):
    def post(self, request):
        project = models.QuarterProject.objects.get(pk = request.POST['project'])
        negotiation  = models.Negotiation.objects.get(pk = request.POST['negotiation'])
        if request.POST['status'] == 'approved':
            negotiation.status = 'approved'
            negotiation.save()
            project.status = 'waiting_for_designs'
            project.save()
            messages.success(request , 'تم الحفظ !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.POST['status'] == 'rejected':
            negotiation.status = 'rejected'
            negotiation.save()
            project.status = 'canceled'
            project.save()
            messages.danger(request , 'تم الغاء الطلب  !')
            return redirect(reverse_lazy('quarter:projet_list'))
            
            
# attach designes 


#confirm work start 


#confirm project 


##update status 

