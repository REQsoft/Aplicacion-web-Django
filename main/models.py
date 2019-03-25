from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from connections.models import Connection
import ldap

#==============================Autenticación===========================

class AuthenticationDB(models.Model):
    name = models.SlugField(primary_key=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, default=None, null=True)
    table_users = models.CharField(max_length=30, blank=True)
    field_username = models.CharField(max_length=30, blank=True)
    field_password = models.CharField(max_length=30, blank=True) 
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'AuthenticationDB'
        verbose_name_plural = 'AuthenticationDB'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("authdb-update")
    
    def save(self, *args, **kwargs):

        super(AuthenticationDB, self).save()
        if self.is_active == True:
            try:
                authdb = AuthenticationLDAP.objects.get(name='AuthenticationLDAP')
                authdb.is_active = False
                authdb.save()
            except:
                pass

    def get_query_search(self):
        return """select %(field_username)s, %(field_password)s from %(table_users)s 
        where %(field_username)s=%(u)s""" %{
                "field_username":self.field_username,
                "field_password":self.field_password,
                "table_users":self.table_users,
                "u":"%(username)s"
            }

    def get_query_auth(self):
        return """select %(field_username)s, %(field_password)s from %(table_users)s 
        where %(field_username)s=%(u)s and %(field_password)s=%(p)s""" %{
                "field_username":self.field_username,
                "field_password":self.field_password,
                "table_users":self.table_users,
                "u":"%(username)s",
                "p":"%(password)s"
            }

    def validate_user(self, username, password):
        conn = self.connection.get_connection()
        if conn is not None:
            data = conn.managerSQL(self.get_query_auth(), input={
            'username':username,
            'password':password})
            if len(data) == 1 and data is not None:
                return True
        return False

    def search_user(self, username):
        conn = self.connection.get_connection()
        if conn is not None:
            data = conn.managerSQL(self.get_query_search(), input={'username':username})
            if len(data) == 1 and data is not None:
                return True
        return False


class AuthenticationLDAP(models.Model):
    types_bind = (
        ('1', 'Enlace directo'),
        ('2', 'Busqueda/Enlace')
    )

    name = models.SlugField(primary_key=True)
    SERVER_URI = models.CharField(max_length=100, blank=True)
    USER_DN_TEMPLATE = models.CharField(max_length=100, blank=True)
    GROUP_SEARCH = models.CharField(max_length=100, blank=True)
    PERMIT_EMPTY_PASSWORD = models.BooleanField(default=False)
    REQUIRE_GROUP = models.CharField(max_length=100, blank=True)
    DENY_GROUP = models.CharField(max_length=100, blank=True)
    authentication = models.CharField(choices=types_bind, max_length=20, default='1')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'AuthenticationLDAP'
        verbose_name_plural = 'AuthenticationLDAP'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("authldap-update")

    def save(self, *args, **kwargs):

        super(AuthenticationLDAP, self).save()
        if self.is_active == True:
            try:
                authdb = AuthenticationDB.objects.get(name='AuthenticationDB')
                authdb.is_active = False
                authdb.save()
            except:
                pass


class LDAPUserSearch(models.Model):
    USER_SEARCH  = models.CharField(max_length=100)
    filter_attr = models.CharField(max_length=100, default=None)

    class Meta:

        verbose_name = 'LDAPSearch'
        verbose_name_plural = 'LDAPSearchs'

    def __str__(self):
        return self.USER_SEARCH

    def get_absolute_url(self):
        return reverse("authldap-update")


#==============================Grupos===========================

class DBGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sql_check_user = models.TextField(blank=True)

    class Meta:
        verbose_name = 'DBGroup'
        verbose_name_plural = 'DBGroups'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("list-connections")

    def search_user(self, username):
        auth = AuthenticationDB.objects.get(name='AuthenticationDB')
        conn = auth.connection.get_connection()
        if conn is not None:
            data = conn.managerSQL(self.sql_check_user, input={'username':username})
            if len(data) == 1 and data is not None:
                return True
        return False

    
class LDAPGroup(models.Model):
    types_bind = (
        (1, 'Enlace directo'),
        (2, 'Busqueda/Enlace')
    )

    name = models.CharField(max_length=100, unique=True)
    USER_DN_TEMPLATE = models.CharField(max_length=100, blank=True)
    type_bind = models.CharField(choices=types_bind, max_length=20, default=1)

    class Meta:
        verbose_name = 'LDAPGroup'
        verbose_name_plural = 'LDAPGroups'

    def __str__(self):
        return self.name

    def search_user(self, username):
        auth =  AuthenticationLDAP.objects.get(name='AuthenticationLDAP')
        uri = auth.SERVER_URI
        conn = ldap.initialize(uri)
        if self.type_bind == 1:
            result = con.search_s(self.USER_DN_TEMPLATE % {'user':username}, 0)
            if len(result) == 1 and result is not None:
                return True
            return False
        
        user_searchs = self.user_search.all()
        if user_searchs is not None:
            for user_search in user_searchs:
                result = con.search_s(user_search.dn_base, 2, user_search.get_filter_attr() % {'user':username})
                if len(result) == 1 and result is not None:
                    return True
            return False
        

    
class LDAPGroupUserSearch(models.Model):
    ldapgroup = models.ForeignKey(LDAPGroup, on_delete=models.CASCADE, related_name='user_search')
    dn_base = models.CharField(max_length=100)
    filter_attr = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name = 'LDAPGroupUserSearch'
        verbose_name_plural = 'LDAPGroupUserSearchs'

    def __str__(self):
        return self.ldapgroup.name

    def get_absolute_url(self):
        return reverse("list-connections")
    
    def get_filter_attr(self):
        return "("+self.filter_attr+"=%(user)s)"






