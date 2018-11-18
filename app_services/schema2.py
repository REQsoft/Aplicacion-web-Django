import graphene
from .models import SQLQuery, Service
from .resolve import *
from promise import Promise
from promise.dataloader import DataLoader
from graphql_jwt.decorators import login_required

queries = SQLQuery.objects.all()
dict_types = {}
dict_clsattr_SQLServicesType = {}
dict_dataloader = {}


def build_loader(service):
    attr = {}
    exec(batch_load_fn(service.service_name), globals(), attr)
    loader = type("DataLoader", (DataLoader,), attr)
    dict_dataloader.update({service.service_name: loader()})


# Esta funcion crea un diccionario con los campos y funciones resolvedoras de un servicio
def build_dict_fields(service):
    clsattr_service = {}

    clsattr_service.update({"name": graphene.String()})
    clsattr_service.update({"kind": graphene.String()})
    clsattr_service.update({"state": graphene.String()})
    clsattr_service.update({"description": graphene.String()})
    clsattr_service.update({"roles": graphene.String()})
    clsattr_service.update(
        {
            "data": graphene.List(
                build_type(service),
                dict.fromkeys(service.get_fields_service(), graphene.String()),
            )
        }
    )

    clsattr_service.update(
        {"resolve_name": lambda self, info, **kwargs: self.Service.name}
    )
    clsattr_service.update(
        {"resolve_kind": lambda self, info, **kwargs: self.Service.kind}
    )
    clsattr_service.update(
        {"resolve_state": lambda self, info, **kwargs: self.Service.state}
    )
    clsattr_service.update(
        {"resolve_descriptio": lambda self, info, **kwargs: self.Service.description}
    )
    clsattr_service.update(
        {"resolve_roles": lambda self, info, **kwargs: self.Service.roles}
    )
    clsattr_service.update(
        {"resolve_data": lambda self, info, **kwargs: self.get_list_search(kwargs)}
    )

    return clsattr_service


def build_service(service):
    if service not in dict_types:
        dict_types.update(
            {
                service: type(
                    service.type_name,
                    (graphene.ObjectType,),
                    build_dict_fields(service),
                )
            }
        )
    return dict_types[service]


def build_type(service):
    clsattr_service = {}
    fields_service = service.get_fields_service()

    if fields_service is not None:
        for field in fields_service:
            clsattr_service.update({field: graphene.String()})
            attr = {}
            clsattr_service.update(
                {"resolve_" + field: lambda self, info, **kwargs: self[info.field_name]}
            )
        """
        links = service.get_links()
        if links is not None:
            for key, value in links.items():
                linked_service = Service.objects.get(service_name=key)
                clsattr_service.update(
                    {
                        key: graphene.List(
                            build_service(linked_service),
                            dict.fromkeys(
                                linked_service.get_fields_service(), graphene.String()
                            ),
                        )
                    }
                )

                attr = {}
                exec(resolve_service_loader(key, value), globals(), attr)
                clsattr_service.update(attr)

                build_loader(linked_service)
                """

    return type(service.type_name + "Data", (graphene.ObjectType,), clsattr_service)


def build_clsattr_SQLServicesType():
    for query in queries:
        if query.is_active():
            try:
                dict_clsattr_SQLServicesType.update(
                    {query.type_name: graphene.Field(build_service(query))}
                )

                dict_clsattr_SQLServicesType.update(
                    {
                        "resolve_"
                        + query.type_name: lambda self, info, **kwargs: self.get(
                            type_name=info.field_name
                        )
                    }
                )
            except:
                print("Algo salio mal")


build_clsattr_SQLServicesType()


class Query(graphene.ObjectType):
    if len(queries) != 0:
        SQLServices = graphene.Field(
            type("SQLServices", (graphene.ObjectType,), dict_clsattr_SQLServicesType)
        )

    user = graphene.String(token=graphene.String())

    def resolve_SQLServices(self, info, **kwargs):
        print(info.context.user)
        return SQLQuery.objects.all()

    def resolve_user(self, info, **kwargs):
        '''token = kwargs.get('token')
        from django.contrib import auth
        user = auth.authenticate(request=info.context, token=token)
        print(user)'''
        return info.context.user

