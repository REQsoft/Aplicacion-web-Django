from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .models import Connection
from .forms import ConnectionForm
from global_.manager_connection import ManagerConnection
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.

#Esta vista muestra el menu principal para las gestion de conexiones
def base_connection(request):
    return render(request, "01Connection/base.html")

#Esta viste muestra el formulario para la creacion de conexiones
class ConnectionCreateView(CreateView):
    model = Connection
    form_class = ConnectionForm
    template_name = "01Connection/connection_form.html"

#Esta vista permite actualizar los datos de una conexion creada
class ConnectionUpdateView(UpdateView):
    model = Connection
    form_class = ConnectionForm
    template_name = "01Connection/connection_form.html"

#Esta vista muestra la lista de conexiones creadas
class ConnectionListView(ListView):
    model = Connection
    template_name = "01Connection/connection_list.html"

#Esta vista permite mostrar la lista de conexiones para el test de conexion
class ConnectionTestView(ListView):
    model = Connection
    template_name = "01Connection/connection_test.html"

#Vista que permite eliminar una conexion
class ConnectionDeleteView(DeleteView):
    model = Connection
    template_name = "01Connection/delete_connection.html"
    success_url = reverse_lazy('list-connections')


#Esta vista permite listar las bases de datos de una conexion
def list_db(request):
    manager_db = request.POST['manager_db']
    user = request.POST['user']
    passwd = request.POST['passwd']
    port = request.POST['port']
    host = request.POST['host']

    conn = ManagerConnection(manager_db,user,passwd,port,host)
    context = {}
    dblist = conn.list_db()      
    if dblist is not None:                
        context =  {'object_list':dblist} 
    return JsonResponse(context)

#Esta vista valida si una conexion es correcta
def check_connection(request, id_connection):
    connection = Connection.objects.get(id=id_connection)
    conn = ManagerConnection(connection.manager_db,connection.user,connection.passwd,connection.port,connection.host,connection.dbname)        
    context =  {'object':conn.check_connection()}
    return JsonResponse(context) 

#Esta vista ejecuta una consulta de prueba para testear una conexion
def test_connection(request):
    id_connection = request.POST['connection']
    query = request.POST['query']
    connection = Connection.objects.get(id=id_connection)
    conn = ManagerConnection(connection.manager_db,connection.user,connection.passwd,connection.port,connection.host,connection.dbname)
    context =  {'object_list':conn.managerSQL(query)}
    return render(request, "01Connection/query_test.html", context) 
