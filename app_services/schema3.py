import graphene
from .models import SQLQuery, Service
from .resolve import *
from promise import Promise
from promise.dataloader import DataLoader
from graphql_jwt.decorators import login_required

queries = SQLQuery.objects.all()
dict_types = {}
build_clsattr_GenericType = {}

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

    return type(service.type_name, (graphene.ObjectType,), clsattr_service)


def build_clsattr_SQLServicesType():
    for query in queries:
        if query.is_active():
            try:
                build_clsattr_GenericType.update(
                    {query.type_name: graphene.Field(build_type(query))}
                )

                build_clsattr_GenericType.update(
                    {
                        "resolve_"
                        + query.type_name: lambda self, info, **kwargs: self.get(type_name=info.field_name).get_list_search(kwargs)
                    }
                )
            except:
                print("Algo salio mal")


build_clsattr_SQLServicesType()


class Query(graphene.ObjectType):
    if len(queries) != 0:
        SQLServices = graphene.Field(
            type("SQLServices", (graphene.ObjectType,), build_clsattr_GenericType)
        )

    user = graphene.String(token=graphene.String())

    def resolve_SQLServices(self, info, **kwargs):
        print(info.context.user)
        return SQLQuery.objects.all()

    def resolve_user(self, info, **kwargs):
        """token = kwargs.get('token')
        from django.contrib import auth
        user = auth.authenticate(request=info.context, token=token)
        print(user)"""
        return info.context.user


