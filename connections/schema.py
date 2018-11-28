import graphene
from services.models import Service, SQLQuery
from .resolve import *
from promise import Promise
from promise.dataloader import DataLoader
from graphql_jwt.decorators import login_required

sql_queries = SQLQuery.objects.all()

#Funcion que construye una clase con los campos de una consulta sql como atributos y crea
#sus respectivos resolvedores

def build_type_data_service(query):
    clsattr_service = {}
    fields_service = query.fields.all()

    for field in fields_service:
        clsattr_service.update({field.name: graphene.String()})
        attr = {}
        clsattr_service.update(
            {"resolve_" + field.name: lambda self, info, **kwargs: self[info.field_name]}
        )

    return type(query.type_name+"Data", (graphene.ObjectType,), clsattr_service)


def build_dict_fields(service):
    clsattr_service = {}

    clsattr_service.update({"theme": graphene.String()})
    clsattr_service.update(
        {
            "data": graphene.List(
                build_type_data_service(service),
                dict.fromkeys(service.get_fields_service(), graphene.String()),
            )
        }
    )

    clsattr_service.update(
        {"resolve_theme": lambda self, info, **kwargs: self.theme}
    )
    clsattr_service.update(
        {"resolve_data": lambda self, info, **kwargs: self.get_list_search(kwargs)}
    )

    return clsattr_service


def build_clsattr_sqltype():
    dict_clsattr_sqltype = {}

    for query in sql_queries:
        if query.is_online():
            dict_clsattr_sqltype.update(
                {
                    query.type_name: 
                    graphene.Field(type(
                        query.type_name,
                        (graphene.ObjectType,),
                        build_dict_fields(query),
                    ))
                }
            )

            dict_clsattr_sqltype.update(
                {
                    "resolve_" + query.type_name: 
                    lambda self, info, **kwargs:
                    self.get(type_name=info.field_name)
                }
            )
    return dict_clsattr_sqltype


if len(sql_queries) > 0:
    class Query(graphene.ObjectType):
        sql = graphene.Field(
            type("SqlType", (graphene.ObjectType,), build_clsattr_sqltype())
        )

        def resolve_sql(self, info, **kwargs):
            return sql_queries
else:

    class Query(graphene.ObjectType):
        pass

