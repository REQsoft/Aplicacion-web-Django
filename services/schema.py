import graphene
from graphene_django.types import DjangoObjectType
from .models import *
from django.contrib import auth
from global_.manager_connection import ManagerConnection
from . import schema_home as schema

class LocationType(DjangoObjectType):
    class Meta:
        model = Location

class MissingItemType(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    photo = graphene.String()

    def resolve_title(self, info, **kwargs):
        return self.title

    def resolve_description(self, info, **kwargs):
        return self.description
    
    def resolve_photo(self, info, **kwargs):
        return self.photo.url


class ServiceType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    icon = graphene.String()
    kind = graphene.String()
    description = graphene.String()
    

    def resolve_id(self, info, **kwargs):
        return self.id
    
    def resolve_kind(self, info, **kwargs):
        return self.kind

    def resolve_title(self, info, **kwargs):
        return self.title

    def resolve_icon(self, info, **kwargs):
        return self.icon.image.url

    def resolve_description(self, info, **kwargs):
        return self.description


class WidgetType(graphene.ObjectType):
    id = graphene.Int()
    ofType = graphene.String()
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
        try:
            if self.ofType == 'menu':
                return self.menu.title

            if self.ofType == 'button':
                return self.button.service.title
        except:
            return None
    
    def resolve_icon(self, info, **kwargs):
        try:
            if self.ofType == 'menu':
                return self.menu.icon.image.url

            if self.ofType == 'button':
                return self.button.service.icon.image.url
        except:
            return None
    
    def resolve_description(self, info, **kwargs):
        try:
            if self.ofType == 'menu':
                return self.menu.description

            if self.ofType == 'button':
                return self.button.service.description
        except:
            return None

    
    def resolve_services(self, info, **kwargs):
        try:
            if self.ofType == 'menu':
                return self.menu.services.all()

            if self.ofType == 'button':
                return [self.button.service]
        except:
            return []

def check_user_group(group, username):
    data_connection = group.connection.get_data_connection()
    conn = ManagerConnection(**data_connection)
    data = conn.managerSQL(group.sql_get_user, input={'username':username})
    if data is None or len(data) == 0:
        return False
    return True

class ContainerType(graphene.ObjectType):
    name = graphene.String()
    widgets = graphene.List(WidgetType, id=graphene.Int())

    def resolve_name(self, info, **kwargs):
        return self.name
    
    def resolve_widgets(self, info, **kwargs):
        user = info.context.user.username
        widgets = []

        if user == 'AnonymousUser':
            return self.widget_set.filter(groups=None)
            
        for widget in self.widget_set.all():
            groups = widget.groups.all()
            if len(groups) == 0:
                widgets.append(widget)
            else:
                for group in groups:
                    if check_user_group(group, user):
                        widgets.append(widget)
                        break           
        return widgets



class Query(schema.Query, graphene.ObjectType):
    containers = graphene.List(ContainerType, name=graphene.String())
    
    map = graphene.List(LocationType, service=graphene.Int(required=True))
    catalog = graphene.List(MissingItemType, service=graphene.Int(required=True))


    def resolve_containers(self, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return [Container.objects.get(name=name)] 
        return Container.objects.all()
    
    def resolve_directory(self, info, **kwargs):
        user = info.context.user
        print(user)
        service_id = kwargs.get('service')
        try:
            service = Service.objects.get(id=service_id)
            widget = None
            try:
                button = service.button
                widget = button.widget  
            except:
                pass
            
            try:
                menu = service.menu
                widget = menu.widget  
            except:
                pass
            
            if widget is not None:
                if str(user) == 'AnonymousUser':
                    if widget.group is None:
                        return Office.objects.filter(service=service)
                
                groups = widget.groups.all()
                if len(groups) == 0:
                    return Office.objects.filter(service=service)

                for group in groups:
                    if check_user_group(group, user):
                        return Office.objects.filter(service=service)                       
        except:
            return []  
        return []

    def resolve_map(self, info, **kwargs):
        user = info.context.user
        print(user)
        service_id = kwargs.get('service')
        try:
            service = Service.objects.get(id=service_id)
            widget = None
            try:
                button = service.button
                widget = button.widget  
            except:
                pass
            
            try:
                menu = service.menu
                widget = menu.widget  
            except:
                pass
            
            if widget is not None:
                if str(user) == 'AnonymousUser':
                    if widget.group is None:
                        return Location.objects.filter(service=service)
                
                groups = widget.groups.all()
                if len(groups) == 0:
                    return Location.objects.filter(service=service)

                for group in groups:
                    if check_user_group(group, user):
                        return Location.objects.filter(service=service)                       
        except:
            return []  
        return []

    def resolve_catalog(self, info, **kwargs):
        user = info.context.user
        print(user)
        service_id = kwargs.get('service')
        try:
            service = Service.objects.get(id=service_id)
            widget = None
            try:
                button = service.button
                widget = button.widget  
            except:
                pass
            
            try:
                menu = service.menu
                widget = menu.widget  
            except:
                pass
            
            if widget is not None:
                if str(user) == 'AnonymousUser':
                    if widget.group is None:
                        return MissingItem.objects.filter(service=service)
                
                groups = widget.groups.all()
                if len(groups) == 0:
                    return MissingItem.objects.filter(service=service)

                for group in groups:
                    if check_user_group(group, user):
                        return MissingItem.objects.filter(service=service)                       
        except:
            return []  
        return []