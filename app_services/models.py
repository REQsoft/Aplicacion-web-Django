from django.db import models
from django.urls import reverse
from global_.manager_connection import ManagerConnection
from main.models import Group
from app_connection.models import Connection
import ast

class Icon(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='icons')

    def __str__(self):
        return self.title

class Kind(models.Model):
    id = models.SlugField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title

# Modelo principal de servicios.
class Service(models.Model):
    title = models.CharField(max_length=100, unique=True)
    icon = models.ForeignKey(Icon, on_delete="PROTECTED")
    kind = models.ForeignKey(Kind, on_delete="PROTECTED")
    description = models.CharField(max_length=300, blank=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service-list')

class Container(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name

class Widget(models.Model):
    widgetsType  = (
        ('menu', 'Menu'),
        ('button', 'Botón')
    )

    ofType = models.CharField(choices=widgetsType, max_length=20)
    title = models.CharField(max_length=100, unique=True)
    icon = models.ForeignKey(Icon, on_delete="PROTECTED")
    state = models.BooleanField(default=False)
    description = models.CharField(max_length=300, blank=True)
    container = models.ForeignKey(Container, on_delete="PROTECTED")
    groups = models.ManyToManyField(Group, blank=True)


    class Meta:
        """Meta definition for Widget."""

        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'

    def __str__(self):
        return self.title

# Modelos de widgets para mostrar los servicios en la app movil
class Menu(models.Model):
    widget = models.OneToOneField(Widget, on_delete=models.CASCADE, limit_choices_to={'ofType':'menu'}, related_name='menus')
    services = models.ManyToManyField(Service)
    
    def __str__(self):
        return self.widget.title


class Button(models.Model):
    widget = models.OneToOneField(Widget, on_delete=models.CASCADE, limit_choices_to={'ofType':'button'})
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.widget.title    

# Modelo de configuracion de servicios de consulta SQL
class SQLQuery(models.Model):
    service = models.OneToOneField(Service, primary_key=True, on_delete="CASCADE",
                                    limit_choices_to={'kind': 'query'},
                                    related_name="query", related_query_name="query")
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    type_name = models.CharField(max_length=50, unique=True)
    query_sql = models.CharField(max_length=300)
    description_fields = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return self.type_name

    def get_absolute_url(self):
        return reverse("base-service")

    def is_active(self):
        connection = ManagerConnection(**self.connection.get_data_connection())
        return connection.check_connection()

    def get_fields_service(self):
        connection = ManagerConnection(**self.connection.get_data_connection())
        return connection.getColumns(self.query_sql)

    def get_list_search(self, filter={}):
        connection = ManagerConnection(**self.connection.get_data_connection())
        data = connection.managerSQL(self.query_sql)
        
        if data is not None:
            if len(filter) > 0:
                for key, value in filter.items():
                    filtered_data = []
                    for fact in data:
                        if str(fact[key]) == str(value):
                            filtered_data.append(fact)
                    data = filtered_data
            return data
        return None

    def get_links(self):
        if len(self.links) > 0:
            try:
                dict_links = ast.literal_eval(self.links)
                if type(dict_links) is type({}):
                    return dict_links
                return None
            except:
                return None

# Modelos de items individuales, asociados a un servicio general de Objetos Perdidos, Directorio y Geolocalizacion
class MissingItem(models.Model):
    service = models.ForeignKey(Service, on_delete="CASCADE",
                                limit_choices_to={'kind': 'catalog'},
                                related_name="items", related_query_name="item")
    title = models.CharField(max_length=100, unique=True) 
    description = models.CharField(max_length=200) 
    date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service-configure', kwargs={'service_id': service.id})

class Office(models.Model):
    service = models.ForeignKey(Service, on_delete="CASCADE",
                                limit_choices_to={'kind': 'directory'},
                                related_name="offices", related_query_name="office")
    title = models.CharField(max_length=100, unique=True)
    extension = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service-configure', kwargs={'service_id': service.id})

class Location(models.Model):
    service = models.ForeignKey(Service, on_delete="CASCADE",
                                limit_choices_to={'kind': 'map'},
                                related_name="locations", related_query_name="location")
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True)
    icon = models.ForeignKey(Icon, on_delete="PROTECTED", default=None, blank=True)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return redirect(reverse('service-configure', kwargs={'service_id': service.id}))
