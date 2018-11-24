from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *
from django.http import JsonResponse

def base_service(request):
    return render(request, "Services/base.html")

class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff.
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class GetUrlMixin(object):
    """
    Este mixin redireccionara a la pagina de configuracion de cada servicio.
    """
    def get_success_url(self):
        service = self.object.service
        return reverse( 'service-configure', kwargs={'pk': service.id})

# Servicio
def service_configure(request,pk):
    service = get_object_or_404(Service, id=pk)

    if(service.kind=='query'):
        query,state=SQLQuery.objects.get_or_create(service=service)
        return redirect(reverse('query-configure', kwargs={'pk': query.service.id}))

    return render(request, 'Services/'+str(service.kind)+'_configure.html', {'service':service})

def add_element(request,pk):
    service = get_object_or_404(Service, id=pk)
    
    if(service.kind=='catalog'):
        form = MissingItemForm()
        if request.method == 'POST':
            form = MissingItemForm(request.POST, request.FILES)

    elif(service.kind=='directory'):
        form = OfficeForm()
        if request.method == 'POST':
            form = OfficeForm(request.POST)

    elif(service.kind=='map'):
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
    return render(request, 'Services/'+str(service.kind)+'_form.html', {'form':form, 'service':service})

    
class ServiceListView(ListView):
    model = Service
    template_name = "Services/service_list.html"

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "Services/service_form.html"

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "Services/service_form.html"

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "Services/confirm_delete.html"
    success_url = reverse_lazy('service-list')


# Catalogo de objetos perdidos
class MissingItemUpdateView(GetUrlMixin, UpdateView):
    model = MissingItem
    form_class = MissingItemForm
    template_name = "Services/catalog_form.html"

class MissingItemDeleteView(GetUrlMixin, DeleteView):
    model = MissingItem
    template_name = "Services/confirm_delete.html"


# Directorio de dependencias
class OfficeUpdateView(GetUrlMixin, UpdateView):
    model = Office
    form_class = OfficeForm
    template_name = "Services/directory_form.html"

class OfficeDeleteView(GetUrlMixin, DeleteView):
    model = Office
    template_name = "Services/confirm_delete.html"


# Mapa de bloques
class LocationUpdateView(GetUrlMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "Services/map_form.html"

class LocationDeleteView(GetUrlMixin, DeleteView):
    model = Location
    template_name = "Services/confirm_delete.html"


# Consulta SQL

class QueryUpdateView(GetUrlMixin, UpdateView):
    model = SQLQuery
    form_class = QueryForm
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

