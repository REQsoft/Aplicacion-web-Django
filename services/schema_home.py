import graphene
from main.models import AuthenticationDB, AuthenticationLDAP
from webadmin.backends import CustomBackend, LDAPBackend
from .type_models import *



def get_common_attr():
    """ 
    Crear un diccionario con los atributos de clase comunes
    de los campos y funciones resolvedoras para los servicios y carpetas.

    Retorna un diccionario.
    """
    dict_clsattr = {}

    #Common fields
    dict_clsattr.update({"title": graphene.String()})
    dict_clsattr.update({"icon": graphene.String()})
    dict_clsattr.update({"theme": graphene.String()})
    dict_clsattr.update({"state": graphene.Boolean()})
    dict_clsattr.update({"description": graphene.String()})
    

    #Common resolvers
    dict_clsattr.update({"resolve_title": lambda self, info, **kwargs: self.title})
    dict_clsattr.update({"resolve_icon": lambda self, info, **kwargs: self.icon})
    dict_clsattr.update({"resolve_state": lambda self, info, **kwargs: self.state})
    dict_clsattr.update({"resolve_description":lambda self, info, **kwargs: self.description})

    return dict_clsattr


def build_generic_type(service):
    """
    Crear el tipo que representa la informacion
    de un servicio generico.

    Obtiene los atributos de clase de los campos
    y funciones resolvedoras a partir de los campos 
    de la consulta sql.

    :Parámetros:
    service -- servicio generico a representar en esquema graphql

    :Retorno: 
    Retorna una instancia de clase del tipo o "None" si han ocurrido
    errores.
    """
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
    except:
        return None


def get_type_data_service(service):
    """
    Crea un tipo graphql que representa la información
    de un servicio.

    Dependiendo del tema del servicio se asignará
    el tipo correspondiente para su informacion.

    :Parámetros:
    service -- Instancia del servicio.

    :Retorno:
    Para servicios con temas definidos con modelos
    se utilizara los tipos conrrespondientes a cada
    modelo.

    Si el tema del servicio es generico se retornará
    un tipo creado de manera dinámica.

    """
    if service.theme == "generic":
        return build_generic_type(service)
    
    if service.theme == "directory":
        return OfficeType

def get_elements_service(service):
    """

    """
    if service.source == "sql":
        return  service.query.get_list_search()
    
    if service.source == "model":
        if service.theme == "directory":
            return service.offices.all()


def built_type_service(service):
    """
    Crea un tipo graphql que representa un servicio.

    Obtiene los atributos de clase para sus campos 
    y funciones resolvedoras de "get_common_attr".

    Como atributo adicional se adiciona la funcion 
    resolvedora para el campo "theme".

    Se adiciona la función resolvedora para "elements"
    si el servicio contiene información. De lo contrario
    la consulta de "elements" en el esquema retornará
    "null".

    :Parametros:
    service -- Servicio a esquematizar.

    :Retornos:
    - Instancia de clase del tipo graphql del servicio.
    """
    dict_clsattr = get_common_attr()

    dict_clsattr.update({"resolve_theme": lambda self, info, **kwargs: self.theme})

    type_field = get_type_data_service(service)
    if type_field is not None:
        dict_clsattr.update({"elements": graphene.List(type_field)})
        dict_clsattr.update({"resolve_elements": lambda self, info, **kwargs: get_elements_service(self)})

    return type(service.type_name, (graphene.ObjectType,), dict_clsattr)


def get_ldapgroups(element):
    try:
        groups = element.ldapgroups.all()
    except:
        groups = []
    
    return groups


def get_dbgroups(element):
    try:
        groups = element.dbgroups.all()
    except:
        groups = []
    
    return groups


def authenticate_user_in_group(backend, username, groups):
    if len(groups) == 0:
        return True

    for group in groups:
        user = backend.authenticate(username=username, group=group)
        if user is not None:
            return True
    return False

def check_group(element, username):
    """
    Valida los permisos de un usuario que consulta
    un elemento(carpeta o servicio).

    :Parámetros: 
    element -- carpeta o servicio consultado.
    username -- nombre de usuario que consulta el elemento.

    :Retornos:
    - Retorna el elemento si el usuario tiene permisos para
    su consulta.
    - Retorna una excepción si el usuario no tiene permisos.

    Excepciones:
    #100 -- El usuario no tiene permisos para la consulta
    #200 -- Sistema de autenticación no configurado
    """

    username = str(username)

    try:
        authdb = AuthenticationDB.objects.get(name='AuthenticationDB')
    except:
        authdb = None

    try:
        authldap = AuthenticationLDAP.objects.get(name='AuthenticationLDAP')
    except:
        authldap = None


#============== Validación de usuario anónimo =====================

    if username == "AnonymousUser":
        if authdb is not None: 
            if authdb.is_active:
                groups = get_dbgroups(element)
                if len(groups) == 0:
                    return element
                else:
                    raise "Error #100"

        if authldap is not None:
            if authldap.is_active:
                groups = get_ldapgroups(element)
                if len(groups) == 0:
                    return element
                else:
                    raise "Error #100"

        return element


        
#============== Validación de usuarios autenticados =====================

    if authdb is not None:
        if authdb.is_active:
            groups = get_dbgroups(element)
            if len(groups) > 0:
                if not authenticate_user_in_group(CustomBackend(), username, groups):
                    raise "Error #100"
            return element
    
    if authldap is not None:
        if authdb.is_active:
            groups = get_ldapgroups(element)
            if len(groups) > 0:
                if not authenticate_user_in_group(LDAPBackend(), username, groups):
                    raise "Error #100"
            return element

    return element


def get_elements_folder(folder):
    """
    Crea un diccionario con los elementos que tienen una 
    carpeta.

    :Parámetros:
    folder -- La carpeta padre de los elementos

    :Retorno:
    - Retorna un diccionario de elementos:
        llave: folders, valor: lista de carpetas de la carpeta
        llave: services, valor: lista de servicios de la carpeta
    """
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


def build_type_elements(folder):
    """
    Crea un tipo graphql de los elementos de una
    carpeta. Sus atributos de clase corresponden 
    a los campos y funciones resolvedoras de cada
    elemento de la carpeta (sea una carpeta o servicio).

    :Parámetros:
    folder -- La carpeta padre de los elementos

    :Retornos:
    - Instancia de clase del tipo graphql de los elementos
    de la carpeta
    - None si la carpeta no tienen elementos
    """
    
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
                lambda self, info, **kwargs: check_group(self['services'].get(type_name=info.field_name), info.context.user)
            })

    for f in folders:
        type_folder = build_type_folder(f)
        dict_clsattr.update({f.type_name:graphene.Field(type_folder)})

        dict_clsattr.update({
            "resolve_"+f.type_name: 
            lambda self, info, **kwargs: check_group(self['folders'].get(type_name=info.field_name), info.context.user)
        })
        
    if len(dict_clsattr) > 0:
        return type(
            folder.type_name + "Elements",
            (graphene.ObjectType,),
            dict_clsattr
        )
    return None

def build_type_folder(folder):
    """
    Crea un tipo graphql que representa una carpeta.

    Obtiene los atributos de clase para sus campos 
    y funciones resolvedoras de "get_common_attr"

    Se adiciona el campo "elements" y su función resolvedora
    si la carpeta contiene elementos.

    :Parametros:
    folder -- Carpeta a esquematizar.

    :Retornos:
    - Instancia de clase del tipo graphql de la carpeta
    """

    dict_clsattr = get_common_attr()

    type_elements_folder = build_type_elements(folder)
    if type_elements_folder is not None:
        dict_clsattr.update({"elements": graphene.Field(type_elements_folder)})
        dict_clsattr.update({
            "resolve_elements": 
            lambda self, info, **kwargs:get_elements_folder(self)
         })

    return type(folder.type_name, (graphene.ObjectType, ), dict_clsattr)


try:
    home = Folder.objects.get(type_name='Home')
    type_home = build_type_folder(home)

    class Query(graphene.ObjectType):
        Home = graphene.Field(type_home)

        def resolve_Home(self, info, **kwargs):
            return check_group(home, info.context.user)
except Exception as e:
    print(e)
    class Query(graphene.ObjectType):
        Home = graphene.String()




