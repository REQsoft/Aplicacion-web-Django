from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from global_.manager_connection import ManagerConnection
from main.models import Group, AuthenticationDB
from graphql_jwt.utils import get_credentials, get_payload
from graphql_jwt.settings import jwt_settings
from django_auth_ldap.backend import LDAPBackend, logger, _LDAPUser, LDAPSettings
import ldap

def get_user_by_natural_key(user_id):
    try:
        auth = AuthenticationDB.objects.all()[0]
        data_connection = auth.connection.get_data_connection()
        data_connection.update({"dbname": auth.connection.dbname})
        conn = ManagerConnection(**data_connection)
        data = conn.managerSQL(auth.sql_auth_user, input={'username':user_id})
        if data is not None:
            return User(username=user_id)
        return None
    except:
        return None


def get_user_by_payload(payload):
    username = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)

    if not username:
        raise exceptions.JSONWebTokenError(_("Invalid payload"))

    user = get_user_by_natural_key(username)

    if user is not None and not user.is_active:
        raise exceptions.JSONWebTokenError(_("User is disabled"))
    return user


def check_user(username, password):
    auth = AuthenticationDB.objects.all()[0]
    data_connection = auth.connection.get_data_connection()
    conn = ManagerConnection(**data_connection)
    data = conn.managerSQL(auth.sql_auth, input={'username':username, 'password':password})
    if data is None or len(data) == 0:
        return False
    return True


class CustomBackend(object):
    
    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        try:
            username = kwargs[get_user_model().USERNAME_FIELD]
            password = kwargs["password"]
            if check_user(username, password):
                return User(username=username)
            return None
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class JSONWebTokenBackend(object):

    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        token = get_credentials(request, **kwargs)

        if token is not None:
            payload = get_payload(token, request)
            return get_user_by_payload(payload)

        return None

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)



class LDAPBackend(LDAPBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is None:
            return None

        token = get_credentials(request, **kwargs)

        if token is not None:
            payload = get_payload(token, request)
            username = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)
            ldap_user = _LDAPUser(self, username=username.strip(), request=request)

            if self.settings.USER_SEARCH is not None:
                user_dn = ldap_user._search_for_user_dn()
            elif self.settings.USER_DN_TEMPLATE is not None:
                user_dn = ldap_user._construct_simple_user_dn()
            else:
                user_dn = None

            if user_dn is not None:
                try:
                    result_search = ldap_user.connection.search_s(user_dn, 0)
                    if len(result_search) == 1 and result_search is not None:
                        return User(username=username) 
                except:
                    pass
            return None

        if password or self.settings.PERMIT_EMPTY_PASSWORD:
            ldap_user = _LDAPUser(self, username=username.strip(), request=request)
            user = self.authenticate_ldap_user(ldap_user, password)
        else:
            logger.debug('Rejecting empty password for {}'.format(username))
            user = None

        return user
    
    def get_or_build_user(self, username, ldap_user):
        return (User(username=username), False)