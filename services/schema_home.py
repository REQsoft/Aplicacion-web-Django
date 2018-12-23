import graphene
from .models import *
from promise import Promise
from promise.dataloader import DataLoader
from graphql_jwt.decorators import login_required
from main.models import AuthenticationDB, AuthenticationLDAP


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
                
        if len(dict_clsattr) == 0:
            return None
        return type(service.type_name + "Data", (graphene.ObjectType,), dict_clsattr)
    except Exception as e:
        print(e)
        return None


def get_type_data_field(service):
    if service.theme == "generic":
        return build_generic_type(service)
    
    if service.theme == "directory":
        return OfficeType

def get_resolve_data_field(service):
    if service.source == "sql":
        return lambda self, info, **kwargs: self.query.get_list_search(kwargs)
    
    if service.source == "model":
        if service.theme == "directory":
            return lambda self, info, **kwargs: self.offices.all()


def built_type_service(service):
    dict_clsattr = {}

    dict_clsattr.update({"title": graphene.String()})
    dict_clsattr.update({"icon": graphene.String()})
    dict_clsattr.update({"theme": graphene.String()})
    dict_clsattr.update({"state": graphene.Boolean()})
    dict_clsattr.update({"description": graphene.String()})
    dict_clsattr.update({"elements": graphene.List(type_field)})

    type_field = get_type_data_field(service)
    if type_field is not None:
        dict_clsattr.update({"resolve_elements": get_resolve_data_field(service)})

    dict_clsattr.update({"resolve_title": lambda self, info, **kwargs: self.title})

    dict_clsattr.update({"resolve_icon": lambda self, info, **kwargs: self.icon})

    dict_clsattr.update({"resolve_theme": lambda self, info, **kwargs: self.theme})

    dict_clsattr.update({"resolve_state": lambda self, info, **kwargs: self.state})

    dict_clsattr.update({"resolve_description":lambda self, info, **kwargs: self.description})


    return type(service.type_name, (graphene.ObjectType,), dict_clsattr)


def get_groupsdb_element(element):
    if elements._meta.db_table == 'config_folder':
        try:
            groups = folder.groups.all()
        except:
            groups = []
    else:
        try:
            groups = folder.groups.all()
        except:
            groups = []

def check_user_group(elements, username):

    try:
        authdb = AuthenticationDB.objects.get(name='AuthenticationDB')
    except:
        authdb = None

    try:
        authldap = AuthenticationLDAP.objects.get(name='AuthenticationLDAP')
    except:
        authldap = None

    if authdb is not None:
        if authdb.is_active:
            pass
    
    if authldap is not None:
        if authldap.is_active:
            pass


    for group in groups:
        data_connection = group.connection.get_data_connection()
        conn = ManagerConnection(**data_connection)
        data = conn.managerSQL(group.sql_get_user, input={'username':username})
        if data is not None:
            return folder
    
    if len(groups) == 0:
        return folder
    
    raise Exception("No tienes permisos para esta consulta")

def get_elements_folder(folder, user):
    elements = {}
    try:
        elements.update({'folders':folder.folders.all()})
    except:
        pass
    try:
        elements.update({'services':folder.services.all()})
    except:
        pass
    
    return elements


def build_type_folder(folder):
    dict_clsattr = {}

    dict_clsattr.update({"title": graphene.String()})
    dict_clsattr.update({"icon": graphene.String()})
    dict_clsattr.update({"state": graphene.Boolean()})
    dict_clsattr.update({"theme": graphene.String()})
    dict_clsattr.update({"description": graphene.String()})
    dict_clsattr.update( {"elements": graphene.Field(type_folder)})

    type_folder = build_type_elements(folder)
    if type_folder is not None:
        dict_clsattr.update({
            "resolve_elements": 
            lambda self, info, **kwargs:get_elements_folder(self, info.context.user.username)
         })

    dict_clsattr.update({"resolve_title": lambda self, info, **kwargs: self.title})

    dict_clsattr.update({"resolve_icon": lambda self, info, **kwargs: self.icon})

    dict_clsattr.update({"resolve_state": lambda self, info, **kwargs: self.state})

    dict_clsattr.update({"resolve_description":lambda self, info, **kwargs: self.description})

    return type(folder.type_name, (graphene.ObjectType, ), dict_clsattr)


def build_type_elements(folder):
    dict_clsattr = {}

    try:
        folders = folder.folders.all()
    except:
        folders = []

    try:
        services = folder.services.all()
    except:
        services = []

    for service in services:
        type_service = built_type_service(service)
        dict_clsattr.update({service.type_name: graphene.Field(type_service)})

        dict_clsattr.update({
                "resolve_"+service.type_name: 
                lambda self, info, **kwargs: check_user_group(self['services'].get(type_name=info.field_name), info.context.user.username)
            })

    for f in folders:
        type_folder = build_type_folder(f)
        dict_clsattr.update({f.type_name:graphene.Field(type_folder)})

        dict_clsattr.update({
            "resolve_"+f.type_name: 
            lambda self, info, **kwargs: check_user_group(self['folders'].get(type_name=info.field_name), info.context.user.username)
        })
        
    if len(dict_clsattr) > 0:
        return type(
            folder.type_name + "Elements",
            (graphene.ObjectType,),
            dict_clsattr
        )
    return None


try:
    folder_home = Folder.objects.get(type_name='Home')
    type_folder = build_type_folder(folder_home)

    class Query(graphene.ObjectType):
        Home = graphene.Field(type_folder)

        def resolve_Home(self, info, **kwargs):
            return check_user_group(folder_home, info.context.user.username)
except Exception as e:
    print(e)
    class Query(graphene.ObjectType):
        pass




