from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import *
from itertools import chain

def base_config(request):
    return render(request, "config/base.html")


class ComponentListView(ListView):
    model = Component
    template_name = "config/component_list.html"

def component_configure(request,pk):
    component = get_object_or_404(Component, id=pk)
    widgets = list(chain(Menu.objects.filter(component=component), Button.objects.filter(component=component)))
    return render(request, 'config/component_configure.html', {'component':component,'widgets':widgets})