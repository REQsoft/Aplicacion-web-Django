import graphene
from graphene_django.types import DjangoObjectType
from .models import *


class LocationType(DjangoObjectType):
    class Meta:
        model = Location

class MissingItemType(DjangoObjectType):
    class Meta:
        model = MissingItem

class OfficeType(DjangoObjectType):
    class Meta:
        model = Office
    
class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class ServiceType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    icon = graphene.String()
    kind = graphene.String()
    groups = graphene.List(GroupType)
    state = graphene.Boolean()
    description = graphene.String()

    def resolve_id(self, info, **kwargs):
        return self.id

    def resolve_title(self, info, **kwargs):
        return self.title

    def resolve_icon(self, info, **kwargs):
        return self.icon.image.url
    
    def resolve_kind(self, info, **kwargs):
        if self.kind.id == 'directory':
            return 'OfficeType'
        elif self.kind.id=='catalog':
            return 'MissingItemType'
        elif self.kind.id=='map':
            return 'LocationType'
        elif self.kind.id=='query':
            return 'Pendiente'
        else:
            return 'None'

    def resolve_groups(self, info, **kwargs):
        return self.groups.all()
      
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.description
    
    
class ItemType(graphene.ObjectType):
    service = graphene.Field(ServiceType)

    def resolve_service(self, info, **kwargs):
        return self.service


class MenuType(graphene.ObjectType):
    title = graphene.String()
    icon = graphene.String()
    services = graphene.List(ServiceType)

    def resolve_tittle(self, info, **kwargs):
        return self.title
    
    def resolve_icon(self, info, **kwargs):
        return self.icon.image
    
    def resolve_services(self, info, **kwargs):
        return self.service.all()
    
class Directory(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    icon = graphene.String()
    kind = graphene.String()
    state = graphene.Boolean()
    description = graphene.String()

    def resolve_id(self, info, **kwargs):
        return self.id

    def resolve_title(self, info, **kwargs):
        return self.title

    def resolve_icon(self, info, **kwargs):
        return self.icon.image

    def resolve_kind(self, info, **kwargs):
        return 'OfficeType'

    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.description
    
    def resolve_office(self, info, **kwargs):
        return Office.objects.all().filter(service=self)    

class Directories(graphene.ObjectType):
    directory = graphene.Field(Directory)

    def resolve_directory(self, info, **kwargs):
        return self

class Query(graphene.AbstractType):
    directories = graphene.List(Directories, title=graphene.String())
    services = graphene.List(ServiceType)
    menus = graphene.List(MenuType)

    map = graphene.List(LocationType,id=graphene.Int())
    catalog = graphene.List(MissingItemType,id=graphene.Int())
    directory = graphene.List(OfficeType,id=graphene.Int())

    #location = graphene.Field(LocationType,id=graphene.Int())
    #item = graphene.Field(MissingItemType,id=graphene.Int())
    #office = graphene.Field(OfficeType,id=graphene.Int())


    def resolve_map(self, info, **kwargs):
        id = kwargs.get('id')
        source = None

        if id is not None:
            source = Service.objects.get(pk=id)

        if source is not None:
            return Location.objects.all().filter(service=source)

        return Location.objects.all()

    def resolve_catalog(self, info, **kwargs):
        id = kwargs.get('id')
        source = None

        if id is not None:
            source = Service.objects.get(pk=id)

        if source is not None:
            return MissingItem.objects.all().filter(service=source)

        return MissingItem.objects.all()

    def resolve_directory(self, info, **kwargs):
        id = kwargs.get('id')
        source = None

        if id is not None:
            source = Service.objects.get(pk=id)

        if source is not None:
            return Office.objects.all().filter(service=source)

        return Office.objects.all().order_by('service')
    '''
    def resolve_location(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Location.objects.get(pk=id)

        return None

    def resolve_item(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return MissingItem.objects.get(pk=id)

        return None

    def resolve_office(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Office.objects.get(pk=id)

        return None
    '''
    def resolve_directories(self, info, **kwargs):
        title = kwargs.get('title')
        if title is not None:
            return Service.objects.all().filter(kind=2, title=title)
        return Service.objects.all().filter(kind=2)

    def resolve_services(self, info, **kwargs):
        return Service.objects.all()

    def resolve_menus(self, info, **kwargs):
        return Menu.objects.all()