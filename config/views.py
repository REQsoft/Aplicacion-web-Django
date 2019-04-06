from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import *
from services.models import Service
from services.views import ComponentReverseMixin, RouteMixin, ParentMixin
from .forms import FolderForm
from itertools import chain

class FolderFilter(object):
    """
    Al editar una carpeta, este mixin filtra, mediante recursividad, todas las carpetas hijas para evitar ciclos.
    """
    folders = []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.folders = self.get_folders(self.object) | Folder.objects.filter(id=self.object.id)
        context['folders'] = Folder.objects.exclude(id__in=self.folders)
        return context

    def get_folders(self, folder):
        self.folders = Folder.objects.filter(folder=folder)
        for folder in self.folders:
            self.folders = self.folders | self.get_folders(folder)
        return self.folders

def base_config(request):
    return render(request, "components/base.html")

class FolderCreateView(RouteMixin,ParentMixin,ComponentReverseMixin,CreateView):
    model = Folder
    form_class = FolderForm
    template_name = "components/component_form.html"
    route = 'folder-create'

class FolderUpdateView(RouteMixin,FolderFilter,ParentMixin,ComponentReverseMixin,UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = "components/component_form.html"
    route = 'folder-edit'

class FolderDeleteView(RouteMixin,ComponentReverseMixin,DeleteView):
    model = Folder
    template_name = "Services/confirm_delete.html"
    success_url = reverse_lazy('component-list')
    route = 'folder-delete'

def component_list(request,pk):
    folder = get_object_or_404(Folder, id=pk)
    services = Service.objects.filter(folder=folder)
    folders = Folder.objects.filter(folder=folder)
    return render(request, 'components/component_list.html', {'self':folder,'folders':folders,'services':services})


# def color_css(request, color):
#    """
#    Create a css file based on a color criteria,
#    or any other complicated calculations necessary
#    """
#    # do custom element positionting.
#    return render_to_response('css/color.css', {'color': color})


# # color.css    
# body {
#   background-color: {{ color }}
# }