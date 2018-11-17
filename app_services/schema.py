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
    ofType = graphene.String()
    title = graphene.String()
    icon = graphene.String()
    state = graphene.Boolean()
    description = graphene.String()
    

    def resolve_ofType(self, info, **kwargs):
        return self.ofType
    
    def resolve_title(self, info, **kwargs):
        return self.title
    
    def resolve_icon(self, info, **kwargs):
        return self.icon.url
    
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.description

class ContainerType(graphene.ObjectType):
    name = graphene.String()
    widgets = graphene.List()

    def resolve_name(self, info, **kwargs):
        return self.name
    
    def resolve_widgets(self, info, **kwargs):
        return self.widget_set

class Query(graphene.AbstractType):
    containers = graphene.List(ContainerType)

    menu = graphene.Field(MenuType, id=graphene.Int(required=True))
    button = graphene.Field(Buttontype, id=graphene.Int(required=True))

    def resolve_containers(self, info, **kwargs):
        return Container.objects.all()

    def resolve_menu(self, info, **kwargs):
        return Menu
    
    def resolve_button(self, info, **kwargs):
        for i in Button.objects.all():
            print(i.service.title)
        return Button.objects.all()