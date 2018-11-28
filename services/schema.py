import graphene
from graphene_django.types import DjangoObjectType
from .models import *
from itertools import chain


class PruebaType(graphene.ObjectType):
    title = graphene.String()

    def resolve_title(self, info, **kwargs):
        return self.title

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

class Query(graphene.ObjectType):
    directory = graphene.List(OfficeType, service=graphene.Int(required=True))
    map = graphene.List(LocationType, service=graphene.Int(required=True))
    catalog = graphene.List(MissingItemType, service=graphene.Int(required=True))
    prueba = graphene.List(PruebaType)

    def resolve_prueba(self, info, **kwargs):
        prueba = list(chain(Office.objects.all(), Location.objects.all(), MissingItem.objects.all()))
        return prueba

    def resolve_directory(self, info, **kwargs):
        user = info.context.user
        service_id = kwargs.get('service')
        service = Service.objects.get(id=service_id)
        try:
            groups = service.button.groups.all()
        except:
            groups = service.menu.groups.all()

        if len(groups) == 0:
            return Office.objects.filter(service=service)
        for group in groups:
            if check_user_group(group, user):
                return Office.objects.filter(service=service)                       
        return []

    def resolve_map(self, info, **kwargs):
        user = info.context.user
        service_id = kwargs.get('service')
        service = Service.objects.get(id=service_id)
        try:
            groups = service.button.groups.all()
        except:
            groups = service.menu.groups.all()

        if len(groups) == 0:
            return Location.objects.filter(service=service)
        for group in groups:
            if check_user_group(group, user):
                return Location.objects.filter(service=service)                       
        return []

    def resolve_catalog(self, info, **kwargs):
        user = info.context.user
        service_id = kwargs.get('service')
        service = Service.objects.get(id=service_id)
        try:
            groups = service.button.groups.all()
        except:
            groups = service.menu.groups.all()

        if len(groups) == 0:
            return MissingItem.objects.filter(service=service)
        for group in groups:
            if check_user_group(group, user):
                return MissingItem.objects.filter(service=service)                       
        return []