from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from global_.manager_connection import ManagerConnection
from app_admin.models import Group, Authentication
from graphql_jwt.utils import get_credentials, get_payload
from graphql_jwt.settings import jwt_settings


def get_user_by_natural_key(user_id):
    try:
        groups = Group.objects.all()
        for group in groups:
            data_connection = group.authentication.connection.get_data_connection()
            data_connection.update({"dbname": group.authentication.connection.dbname})
            conn = ManagerConnection(**data_connection)
            data = conn.managerSQL(group.sql_get_user % (user_id))
            if len(data) > 0:
                user = User(username=user_id)
                return user
        return None
    except User.DoesNotExist:
        return None


def get_user_by_payload(payload):
    username = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)

    if not username:
        raise exceptions.JSONWebTokenError(_("Invalid payload"))

    user = get_user_by_natural_key(username)

    if user is not None and not user.is_active:
        raise exceptions.JSONWebTokenError(_("User is disabled"))
    return user


def validate(username, password):
    auth = Authentication.objects.all()[0]
    data_connection = auth.connection.get_data_connection()
    data_connection.update({"dbname": auth.connection.dbname})
    conn = ManagerConnection(**data_connection)
    data = conn.managerSQL(auth.sql_auth % (username, password))
    if len(data) > 0:
        return True
    return False
        

class CustomBackend(object):
    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        try:
            username = kwargs[get_user_model().USERNAME_FIELD]
            password = kwargs["password"]
            if validate(username, password):
                user = User(username=username)
                return user
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