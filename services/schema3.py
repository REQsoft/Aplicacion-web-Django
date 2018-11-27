import graphene
from .models import *
from .resolve import *
from promise import Promise
from promise.dataloader import DataLoader
from graphql_jwt.decorators import login_required

services = Service.objects.all()

# Funcion que construye una clase con los campos de una consulta sql como atributos y crea
# sus respectivos resolvedores

class OfficeType(graphene.ObjectType):
    title = graphene.String()
    extension = graphene.String()
    phone = graphene.String()

    def resolve_title(self, info, **kwargs):
        try:
            return self.title
        except:
            return self['title']

    def resolve_extension(self, info, **kwargs):
        try:
            return self.extension
        except:
            return self['extension']
    
    def resolve_phone(self, info, **kwargs):
        try:
            return self.phone
        except:
            return self['phone']


def build_type_data_service(query):
    clsattr_service = {}
    fields_service = query.query.fields.all()

    for field in fields_service:
        if field.visible:
            clsattr_service.update(
                {field.name: graphene.String(description=field.label)}
            )
            attr = {}
            clsattr_service.update(
                {
                    "resolve_"
                    + field.name: lambda self, info, **kwargs: self[info.field_name]
                }
            )

    if len(clsattr_service) == 0:
        return None
    return type(query.name_type + "Data", (graphene.ObjectType,), clsattr_service)


def build_dict_fields(service):
    clsattr_service = {}

    clsattr_service.update({"title": graphene.String()})
    clsattr_service.update({"icon": graphene.String()})
    clsattr_service.update({"description": graphene.String()})
    clsattr_service.update({"theme": graphene.String()})

    if service.theme == "generic":
        type_service = build_type_data_service(service)
        kwargs_search = dict.fromkeys(service.query.get_fields_service(), graphene.String())
    elif service.theme == "directory":
        type_service = OfficeType
        kwargs_search = {
            "title": graphene.String(),
            "extension": graphene.String(),
            "phone": graphene.String(),
        }
    else:
        type_service = None

    clsattr_service.update({"data": graphene.List(type_service, kwargs_search)})


    clsattr_service.update({"resolve_title": lambda self, info, **kwargs: self.title})

    clsattr_service.update({"resolve_icon": lambda self, info, **kwargs: self.icon})

    clsattr_service.update(
        {"resolve_description": lambda self, info, **kwargs: self.description}
    )

    clsattr_service.update({"resolve_theme": lambda self, info, **kwargs: self.theme})

    if service.data_type == "query":
        resolve_data = lambda self, info, **kwargs: self.query.get_list_search(kwargs)
    elif service.data_type == "models":
        if service.theme == "directory":
            resolve_data = lambda self, info, **kwargs: Office.objects.filter(service=self)
    else:
        resolve_data = None

    clsattr_service.update(
        {"resolve_data": resolve_data}
    )

    return clsattr_service


def build_clsattr_sqltype():
    dict_clsattr_sqltype = {}

    for service in services:

        dict_clsattr_sqltype.update(
            {
                service.name_type: graphene.Field(
                    type(
                        service.name_type,
                        (graphene.ObjectType,),
                        build_dict_fields(service),
                    )
                )
            }
        )

        dict_clsattr_sqltype.update(
            {
                "resolve_"
                + service.name_type: lambda self, info, **kwargs: self.get(
                    name_type=info.field_name
                )
            }
        )
    return dict_clsattr_sqltype


if len(services) > 0:

    class Query(graphene.ObjectType):
        sql = graphene.Field(
            type("Home", (graphene.ObjectType,), build_clsattr_sqltype())
        )

        def resolve_sql(self, info, **kwargs):
            return services


else:

    class Query(graphene.ObjectType):
        pass

