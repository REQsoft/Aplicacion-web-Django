import graphene
from .models import *
from .resolve import *
from promise import Promise
from promise.dataloader import DataLoader
from graphql_jwt.decorators import login_required


class OfficeType(graphene.ObjectType):
    title = graphene.String()
    extension = graphene.String()
    phone = graphene.String()

    def resolve_title(self, info, **kwargs):
        try:
            return self.title
        except:
            return self["title"]

    def resolve_extension(self, info, **kwargs):
        try:
            return self.extension
        except:
            return self["extension"]

    def resolve_phone(self, info, **kwargs):
        try:
            return self.phone
        except:
            return self["phone"]

# ===============================================================================

def build_type_container(container):
    dict_clsattr = {}

    dict_clsattr.update({"title": graphene.String()})
    dict_clsattr.update({"icon": graphene.String()})
    dict_clsattr.update({"description": graphene.String()})

    type_component = build_type_components(container)
    if type_component is not None:
        dict_clsattr.update( {"components": graphene.Field()})

        dict_clsattr.update({
            "resolve_components": 
            lambda self, info, **kwargs:{'services':self.services.all(),
                                        'containers':self.containers.all()}
         })

    return type(container.type_name+"Component", (graphene.ObjectType, ), dict_clsattr)


def build_generic_type(service):
    dict_clsattr = {}

    try:
        fields_type = service.query.fields.all()

        for field in fields_type:
            if field.visible:
                dict_clsattr.update(
                    {field.name: graphene.String(description=field.label)}
                )

                dict_clsattr.update(
                    {
                        "resolve_"
                        + field.name: lambda self, info, **kwargs: self[info.field_name]
                    }
                )
                
        if len(clsattr_service) == 0:
            return None
        return type(query.name_type + "Data", (graphene.ObjectType,), clsattr_service)
    except:
        return None


def get_type_data_field(service):
    if service.theme == "generic":
        return build_generic_type(service)
    
    if service.theme == "directory":
        return OfficeType

def get_resolve_data_field(service):
    if service.source == "sql":
        return lambda self, info, **kwargs: self.query.get_list_search(kwargs)
    
    if service.source == "models":
        if service.theme == "directory":
            return OfficeType


def built_type_service(service):
    dict_clsattr = {}

    dict_clsattr.update({"title": graphene.String()})
    dict_clsattr.update({"icon": graphene.String()})
    dict_clsattr.update({"description": graphene.String()})
    dict_clsattr.update({"theme": graphene.String()})

    type_field = get_type_data_field(service)
    if type_field is not None:
        dict_clsattr.update({"data": graphene.List(type_field)})
        dict_clsattr.update({"resolve_data": get_resolve_data_field(service)})

    dict_clsattr.update({"resolve_title": lambda self, info, **kwargs: self.title})

    dict_clsattr.update({"resolve_icon": lambda self, info, **kwargs: self.icon})

    dict_clsattr.update({"resolve_description":lambda self, info, **kwargs: self.description})

    dict_clsattr.update({"resolve_theme": lambda self, info, **kwargs: self.theme})

    return type(service.type_name, (graphene.ObjectType,), dict_clsattr)


def build_type_components(container):
    dict_clsattr = {}

    try:
        components = container.components.all()
    except:
        components = []
    try:
        services = container.services.all()
    except:
        services = []

    for service in services:
        type_service = built_type_service(service)
        if type_service is not None:
            dict_clsattr.update({service.type_name: graphene.Field(type_service)})

            dict_clsattr.update({
                    "resolve_"+service.type_name: 
                    lambda self, info, **kwargs: self['services'].get(type_name=info.field_name)
                })

    print("#################################")
    for component in components:
        print(component)
        type_component = build_type_container(container)
        if type_component is not None:
            dict_clsattr.update({component.type_name:graphene.Field(type_component)})

            dict_clsattr.update({
                "resolve_"+component.type_name: 
                lambda self, info, **kwargs: self['containers'].get(type_name=info.field_name)
            })
        
    if len(dict_clsattr) > 0:
        return type(
            "HomeComponent",
            (graphene.ObjectType,),
            dict_clsattr
        )
    return None


try:
    container_home = Container.objects.get(type_name='Home')
    type_container = build_type_container(container_home)

    class Query(graphene.ObjectType):
        home = graphene.Field(type_container)

        def resolve_home(self, info, **kwargs):
            return container_home
except Exception as e:
    print(e)
    class Query(graphene.ObjectType):
        pass




