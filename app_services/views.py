from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy,reverse
from .models import *
from .forms import *
from django.http import JsonResponse

def base_service(request):
    return render(request, "Services/base.html")

# Servicio
def service_configure(request,service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'Services/'+str(service.kind.id)+'_configure.html', {'service':service})

def add_element(request,service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if(service.kind.id=='catalog'):
        form = MissingItemForm()
        if request.method == 'POST':
            form = MissingItemForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.service = service
                post.save()
                return redirect(reverse('service-configure', kwargs={'service_id': service.id}))

        #return render(request, 'Services/'+str(service.kind.id)+'_form.html', {'form':form, 'service_id':service_id})

    elif(service.kind.id=='directory'):
        form = OfficeForm()
        if request.method == 'POST':
            form = OfficeForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.service = service
                post.save()
                return redirect(reverse('service-configure', kwargs={'service_id': service.id}))

        #return render(request, 'Services/'+str(service.kind.id)+'_form.html', {'form':form, 'service_id':service_id})

    elif(service.kind.id=='map'):
        form = LocationForm()
        if request.method == 'POST':
            form = LocationForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.service = service
                post.save()
                return redirect(reverse('service-configure', kwargs={'service_id': service.id}))

        #return render(request, 'Services/'+str(service.kind.id)+'_form.html', {'form':form, 'service_id':service_id})
    
    #else:
        #return redirect(reverse('service-configure', kwargs={'service_id': service.id}))
    return render(request, 'Services/'+str(service.kind.id)+'_form.html', {'form':form, 'service':service})

    
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
    success_url = reverse_lazy('service-list')

# Catalogo de objetos perdidos

class MissingItemUpdateView(UpdateView):
    model = MissingItem
    form_class = MissingItemForm
    template_name = "Services/base_form.html"
    def get_success_url(self):
        service = self.object.service
        return reverse_lazy( 'service-configure', kwargs={'service_id': service.id})

class MissingItemDeleteView(DeleteView):
    model = MissingItem
    template_name = "Services/confirm.html"
    def get_success_url(self):
        service = self.object.service
        return reverse_lazy( 'service-configure', kwargs={'service_id': service.id})


# Directorio de dependencias

class OfficeCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "Services/form.html"

class OfficeUpdateView(UpdateView):
    model = Office
    form_class = OfficeForm
    template_name = "Services/base_form.html"
    def get_success_url(self):
        service = self.object.service
        return reverse_lazy( 'service-configure', kwargs={'service_id': service.id})

class OfficeDeleteView(DeleteView):
    model = Office
    template_name = "Services/confirm.html"
    def get_success_url(self):
        service = self.object.service
        return reverse_lazy( 'service-configure', kwargs={'service_id': service.id})

# Mapa de bloques
class LocationCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "Services/service_form.html"

class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "Services/base_form.html"
    def get_success_url(self):
        service = self.object.service
        return reverse_lazy( 'service-configure', kwargs={'service_id': service.id})

class LocationDeleteView(DeleteView):
    model = Location
    template_name = "Services/confirm.html"
    def get_success_url(self):
        service = self.object.service
        return reverse_lazy( 'service-configure', kwargs={'service_id': service.id})


# Consulta SQL

class QueryCreateView(CreateView):
    model = SQLQuery
    form_class = QueryForm
    template_name = "Services/query_configure.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service = Service.objects.get(id=self.kwargs["service_id"])
        self.object.save()
        return super(QueryCreateView, self).form_valid(form)


def get_fields_service(request):
    query_sql = request.POST["query_sql"]
    id_connection = request.POST["connection"]

    connection = Connection.objects.get(id=id_connection)
    data_conecction = connection.get_data_connection()
    conn = ManagerConnection(**data_conecction)
    fields_service = conn.getColumns(query_sql)

    context = {"object_list": fields_service}
    return JsonResponse(context)

