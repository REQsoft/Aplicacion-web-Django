from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import *
from services.models import Service
from services.views import ComponentReverseMixin
from .forms import ComponentForm
from itertools import chain

def base_config(request):
    return render(request, "components/base.html")


class ComponentListView(ListView):
    model = Component
    template_name = "components/component_list.html"

class ComponentCreateView(ComponentReverseMixin,CreateView):
    model = Component
    form_class = ComponentForm
    template_name = "components/component_form.html"

class ComponentUpdateView(ComponentReverseMixin,UpdateView):
    model = Component
    form_class = ComponentForm
    template_name = "components/component_form.html"

class ComponentDeleteView(ComponentReverseMixin,DeleteView):
    model = Component
    template_name = "components/confirm_delete.html"
    success_url = reverse_lazy('component-list')

def component_configure(request,pk):
    component = get_object_or_404(Component, id=pk)
    services = Service.objects.filter(component=component)
    components = Component.objects.filter(component=component)
    return render(request, 'components/component_list.html', {'self':component,'components':components,'services':services})