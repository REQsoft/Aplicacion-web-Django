from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import *
from services.models import Service
from services.views import ComponentReverseMixin
from .forms import FolderForm
from itertools import chain

def base_config(request):
    return render(request, "components/base.html")

class FolderCreateView(ComponentReverseMixin,CreateView):
    model = Folder
    form_class = FolderForm
    template_name = "components/component_form.html"

class FolderUpdateView(ComponentReverseMixin,UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = "components/component_form.html"

class FolderDeleteView(ComponentReverseMixin,DeleteView):
    model = Folder
    template_name = "components/confirm_delete.html"
    success_url = reverse_lazy('component-list')

def component_list(request,pk):
    folder = get_object_or_404(Folder, id=pk)
    services = Service.objects.filter(folder=folder)
    folders = Folder.objects.filter(folder=folder)
    return render(request, 'components/component_list.html', {'self':folder,'folders':folders,'services':services})