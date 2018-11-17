import graphene
from graphene_django.types import DjangoObjectType
from .models import *

class LocationType(DjangoObjectType):
    class Meta:
        model = Location

class MissingItemType(DjangoObjectType):
    class Meta:
        model = MissingItem

class OfficeType(graphene.ObjectType):
    title = graphene.String()
    extension = graphene.String()
    phone = graphene.String()

    def resolve_title(self, info, **kwargs):
        return self.title

    def resolve_extension(self, info, **kwargs):
        return self.extension
    
    def resolve_phone(self, info, **kwargs):
        return self.phone


class ServiceType(graphene.ObjectType):
    title = graphene.String()
    icon = graphene.String()
    description = graphene.String()

    def resolve_title(self, info, **kwargs):
        return self.title

    def resolve_icon(self, info, **kwargs):
        return self.icon.image.url

    def resolve_description(self, info, **kwargs):
        return self.description


class MenuType(graphene.ObjectType):
    services = graphene.List(ServiceType)
    
    def resolve_services(self, info, **kwargs):
        return self.services.all()


class Buttontype(graphene.ObjectType):
    title = graphene.String()
    icon = graphene.String()
    state = graphene.Boolean()
    description = graphene.String()
    service = graphene.Field(ServiceType)

    def resolve_title(self, info, **kwargs):
        return self.service.title
    
    def resolve_icon(self, info, **kwargs):
        return self.service.icon.image.url
    
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.service.description
    
    def resolve_services(self, info, **kwargs):
        return self.service


class WidgetType(graphene.ObjectType):
    id = graphene.Int()
    ofType = graphene.String()
    title = graphene.String()
    icon = graphene.String()
    state = graphene.Boolean()
    description = graphene.String()
    services = graphene.List(ServiceType)

    def resolve_id(self, info, **kwargs):
        return self.id

    def resolve_ofType(self, info, **kwargs):
        return self.ofType
    
    def resolve_title(self, info, **kwargs):
        return self.title
    
    def resolve_icon(self, info, **kwargs):
        return self.icon.image.url
    
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.description
    
    def resolve_services(self, info, **kwargs):
        if self.ofType == 'menu':
            return self.menus.services.all()

        if self.ofType == 'button':
            return [self.button.service]

class ContainerType(graphene.ObjectType):
    name = graphene.String()
    widgets = graphene.List(WidgetType)

    def resolve_name(self, info, **kwargs):
        return self.name
    
    def resolve_widgets(self, info, **kwargs):
        return self.widget_set.all()


class Query(graphene.AbstractType):
    containers = graphene.List(ContainerType, name=graphene.String())

    def resolve_containers(self, info, **kwargs):
        name = kwargs.get('name')
        if name is not None:
            return Container.objects.get(name=name)
        return Container.objects.all()
