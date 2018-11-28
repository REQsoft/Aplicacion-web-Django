import graphene
from graphene_django.types import DjangoObjectType
from .models import *
from services.schema import ServiceType
from django.contrib import auth
from global_.manager_connection import ManagerConnection
from itertools import chain
from operator import itemgetter


class ComponentType(graphene.ObjectType):
    id = graphene.Int()
    state = graphene.Boolean()
    title = graphene.String()
    icon = graphene.String()
    description = graphene.String()
    services = graphene.List(ServiceType)

    def resolve_id(self, info, **kwargs):
        return self.id

    def resolve_ofType(self, info, **kwargs):
        return self.ofType
    
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_title(self, info, **kwargs):
        return self.title
        
    def resolve_icon(self, info, **kwargs):
        return self.icon.image.url    
    
    def resolve_description(self, info, **kwargs):
        return self.description          

    def resolve_services(self, info, **kwargs):
        return self.services.all()       

def check_user_group(group, username):
    data_connection = group.connection.get_data_connection()
    conn = ManagerConnection(**data_connection)
    print("######################################")
    data = conn.managerSQL(group.sql_get_user, input={'username':username})
    if data is None or len(data) == 0:
        return False
    return True

def get_widgets(widgets, user):
    filtered_widgets = []
    print(user)
    for widget in widgets:
        groups = widget.groups.all()
        if len(groups) == 0:
            filtered_widgets.append(widget)
        else:
            for group in groups:
                if check_user_group(group, user):
                    filtered_widgets.append(widget)
                    break           
    return filtered_widgets


class ContainerType(graphene.ObjectType):
    name = graphene.String()
    widgets = graphene.List(WidgetType, id=graphene.Int())

    def resolve_name(self, info, **kwargs):
        return self.name
    
    def resolve_widgets(self, info, **kwargs):
        user = info.context.user
        widgets = list(chain(Menu.objects.filter(container=self), Button.objects.filter(container=self)))
        return get_widgets(widgets,user)

class Query(graphene.ObjectType):
    containers = graphene.List(ContainerType, name=graphene.String())

    def resolve_containers(self, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return [Container.objects.get(name=name)] 
        return Container.objects.all()
    
    