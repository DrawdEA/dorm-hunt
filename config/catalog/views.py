from django.shortcuts import render
from django.views import generic
from .models import School, Dorm, Vouch
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q


# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html", context=context)

class DormsListView(generic.ListView):
    model = Dorm
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        school_name = self.request.GET.get('school')
        if school_name:
            qs = qs.filter(
                Q(schools__name__icontains=school_name) |
                Q(schools__abbreviation__icontains=school_name)
            )
        return qs

class SchoolsListView(generic.ListView):
    model = School
    paginate_by = 10

class DormDetailView(generic.DetailView):
    model = Dorm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dorm = self.get_object()
        vouches = Vouch.objects.filter(dorm=dorm)
        context['vouches'] = vouches
        return context
    
class SchoolDetailView(generic.DetailView):
    model = School

class AllVouchesListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Vouch
    paginate_by = 10
    template_name = "catalog/all_vouch_list.html"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return self.response_class(content='You do not have permission to view this page.', status=403)
        else:
            return super().handle_no_permission()

class MyVouchesListView(LoginRequiredMixin, generic.ListView):
    model = Vouch
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(submitted_by=self.request.user)

class CreateVouch(PermissionRequiredMixin, CreateView):
    model = Vouch
    fields = ["dorm", "rating", "review"]
    permission_required = "catalog.add_vouch"

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)

class UpdateVouch(PermissionRequiredMixin, UpdateView):
    model = Vouch
    fields = ["dorm", "rating", "review"]
    permission_required = "catalog.change_vouch"

class DeleteVouch(PermissionRequiredMixin, DeleteView):
    model = Vouch
    success_url = reverse_lazy("dorm_list")
    permission_required = "catalog.delete_vouch"



class CreateSchool(PermissionRequiredMixin, CreateView):
    model = School
    fields = ["name", "abbreviation", "school_location", "description"]
    permission_required = "catalog.add_school"

class UpdateSchool(PermissionRequiredMixin, UpdateView):
    model = School
    fields = ["name", "abbreviation", "school_location", "description"]
    permission_required = "catalog.change_school"

class DeleteSchool(PermissionRequiredMixin, DeleteView):
    model = School
    success_url = reverse_lazy("index")
    permission_required = "catalog.delete_school"



class CreateDorm(PermissionRequiredMixin, CreateView):
    model = Dorm
    fields = ["name", "schools", "dorm_location", "description"]
    permission_required = "catalog.add_dorm"

class UpdateDorm(PermissionRequiredMixin, UpdateView):
    model = Dorm
    fields = ["name", "schools", "dorm_location", "description"]
    permission_required = "catalog.change_dorm"

class DeleteDorm(PermissionRequiredMixin, DeleteView):
    model = Dorm
    success_url = reverse_lazy("index")
    permission_required = "catalog.delete_dorm"
