from django.db import models
from django.urls import reverse
from global_.manager_connection import ManagerConnection
from main.models import Group
from config.models import Component,Icon
from connections.models import Connection
from django.template.defaultfilters import slugify
import ast

# Modelo principal de servicios.
class Service(models.Model):
    sources = (
        ('sql','Consulta SQL'),
        ('model','Manual'),
    )
    themes = (
        ('generic', 'Generico'),
        ('directory', 'Directorio'),
        ('map', 'Mapa'),
        ('catalog', 'Catalogo'),
    )

    title = models.CharField(max_length=100, unique=True)
    icon = models.ForeignKey(Icon, on_delete="PROTECTED")
    theme = models.CharField(choices=themes, max_length=20)
    component = models.ForeignKey(Component, on_delete='PROTECTED')
    groups = models.ManyToManyField(Group)
    source = models.CharField(choices=sources, max_length=20)
    type_name = models.CharField(max_length=20, unique=True, blank=True)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service-list')
    
    def save(self):

        super(Service, self).save()
        type_name = "S" + str(self.id)

        if self.source == 'sql':
            query_sql = SQLQuery(
                service=self,
            )
            query_sql.save()
        
        self.save()


# Modelo de configuracion de servicios de consulta SQL
class SQLQuery(models.Model):
    service = models.OneToOneField(Service, primary_key=True, on_delete="CASCADE",
                                    limit_choices_to={'source': 'sql'},
                                    related_name="query", related_query_name="query")
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, null=True)
    query_sql = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return self.type_name

    def get_absolute_url(self):
        return reverse("service-list")

    def is_online(self):
        if self.connection is None:
            return False
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
    
    def save(self):
        super(SQLQuery, self).save()
        
        Field.objects.filter(sql_query=self).delete()

        if self.is_online():
            fields_service = self.get_fields_service()

            if fields_service is not None:
                for field in fields_service:
                    field = Field(
                        sql_query = self,
                        name = field,
                        label = field,
                        ofType = 'String'
                    )
                    field.save()
                return
        
                

class Field(models.Model):
    sql_query = models.ForeignKey(SQLQuery, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=20)
    ofType = models.CharField(max_length=10)
    hidden = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'

    def __str__(self):
        return self.name


# Modelos de items individuales, asociados a un servicio general de Objetos Perdidos, Directorio y Geolocalizacion
class MissingItem(models.Model):
    service = models.ForeignKey(Service, on_delete="CASCADE",
                                limit_choices_to={'theme': 'catalog'},
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
                                limit_choices_to={'theme': 'directory'},
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
                                limit_choices_to={'theme': 'map'},
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

