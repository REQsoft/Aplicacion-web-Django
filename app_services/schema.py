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
    title = graphene.String()
    icon = graphene.String()
    state = graphene.Boolean()
    description = graphene.String()
    services = graphene.List(ServiceType)

    def resolve_tittle(self, info, **kwargs):
        return self.title
    
    def resolve_icon(self, info, **kwargs):
        return self.icon.image
    
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.description
    
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
        return self.service.icon.image
    
    def resolve_state(self, info, **kwargs):
        return self.state
    
    def resolve_description(self, info, **kwargs):
        return self.service.description
    
    def resolve_services(self, info, **kwargs):
        return self.service

    

class Query(graphene.AbstractType):
    menus = graphene.List(MenuType)
    buttons = graphene.List(Buttontype)


    def resolve_menus(self, info, **kwargs):
        return Menu.objects.all()
    
    def resolve_buttons(self, info, **kwargs):
        for i in Button.objects.all():
            print(i.service.title)
        return Button.objects.all()