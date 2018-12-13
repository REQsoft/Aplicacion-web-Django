from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json

def base_service(request):
    return render(request, "Services/base.html")

class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff.
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class ServiceReverseMixin(object):
    """
    Este mixin redireccionara a la pagina de configuracion de cada servicio.
    """
    def get_success_url(self):
        service = self.object.service
        return reverse( 'service-configure', kwargs={'pk': service.id})

class ComponentReverseMixin(object):
    """
    Este mixin redireccionara al folder padre.
    """
    def get_success_url(self):
        folder = self.object.folder
        return reverse( 'component-list', kwargs={'pk': folder.id})

# Servicio
def service_configure(request,pk):
    service = get_object_or_404(Service, id=pk)

    if(service.source=='sql'):
        query,state=SQLQuery.objects.get_or_create(service=service)
        return redirect(reverse('query-configure', kwargs={'pk': query.service.id}))

    return render(request, 'Services/'+str(service.theme)+'_configure.html', {'service':service})

def add_element(request,pk):
    service = get_object_or_404(Service, id=pk)
    
    if(service.theme=='catalog'):
        form = MissingItemForm()
        if request.method == 'POST':
            form = MissingItemForm(request.POST, request.FILES)

    elif(service.theme=='directory'):
        form = OfficeForm()
        if request.method == 'POST':
            form = OfficeForm(request.POST)

    elif(service.theme=='map'):
        form = LocationForm()
        if request.method == 'POST':
            form = LocationForm(request.POST)
    
    else:
        return redirect(reverse('service-configure', kwargs={'pk': service.id}))

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.service = service
            post.save()
            return redirect(reverse('service-configure', kwargs={'pk': service.id}))
    return render(request, 'Services/'+str(service.theme)+'_form.html', {'form':form, 'service':service})

    
class ServiceListView(ListView):
    model = Service
    template_name = "Services/service_list.html"

class ServiceCreateView(ComponentReverseMixin,CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "Services/service_form.html"

class ServiceUpdateView(ComponentReverseMixin,UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "Services/service_form.html"

class ServiceDeleteView(ComponentReverseMixin,DeleteView):
    model = Service
    template_name = "Services/confirm_delete.html"
    success_url = reverse_lazy('service-list')


# Catalogo de objetos perdidos
class MissingItemUpdateView(ServiceReverseMixin, UpdateView):
    model = MissingItem
    form_class = MissingItemForm
    template_name = "Services/catalog_form.html"

class MissingItemDeleteView(ServiceReverseMixin, DeleteView):
    model = MissingItem
    template_name = "Services/confirm_delete.html"


# Directorio de dependencias
class OfficeUpdateView(ServiceReverseMixin, UpdateView):
    model = Office
    form_class = OfficeForm
    template_name = "Services/directory_form.html"

class OfficeDeleteView(ServiceReverseMixin, DeleteView):
    model = Office
    template_name = "Services/confirm_delete.html"


# Mapa de bloques
class LocationUpdateView(ServiceReverseMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "Services/map_form.html"

class LocationDeleteView(ServiceReverseMixin, DeleteView):
    model = Location
    template_name = "Services/confirm_delete.html"


# Consulta SQL
class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            print(form.errors)
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            fields = []
            try:
                queryset = Field.objects.filter(sql_query=self.object)
            except:
                pass

            qs_json = serializers.serialize('json', queryset)
    
            return HttpResponse(qs_json, content_type='application/json')
        else:
            return response

class QueryUpdateView(AjaxableResponseMixin, UpdateView):
    model = SQLQuery
    form_class = QueryForm
    template_name = "Services/query_configure.html"

    def get_context_data(self, **kwargs):
        context = super(QueryUpdateView, self).get_context_data(**kwargs)
        try:
            context['fields'] = Field.objects.filter(sql_query=self.object)
        except:
            pass
        return context


class FieldUpdateView(UpdateView):
    model = Field
    form_class = FieldForm
    template_name = "Services/query_configure.html"



def get_fields_service(request):
    query_sql = request.POST["query_sql"]
    id_connection = request.POST["connection"]

    connection = Connection.objects.get(id=id_connection)
    data_conecction = connection.get_data_connection()
    conn = ManagerConnection(**data_conecction)
    fields_service = conn.getColumns(query_sql)

    context = {"object_list": fields_service}
    return JsonResponse(context)

