from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from connections.models import Connection

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
        if len(self.is_active) == True:
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
        if len(self.is_active) == True:
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

    
class LDAPGroup(models.Model):
    types_bind = (
        ('1', 'Enlace directo'),
        ('2', 'Busqueda/Enlace')
    )

    name = models.CharField(max_length=100, unique=True)
    USER_DN_TEMPLATE = models.CharField(max_length=100, blank=True)
    type_bind = models.CharField(choices=types_bind, max_length=20, default='1')

    class Meta:
        verbose_name = 'LDAPGroup'
        verbose_name_plural = 'LDAPGroups'

    def __str__(self):
        return self.name
    
class LDAPGroupUserSearch(models.Model):
    ldapgroup = models.ForeignKey(LDAPGroup, on_delete=models.CASCADE)
    USER_SEARCH  = models.CharField(max_length=100)
    filter_attr = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name = 'LDAPGroupUserSearch'
        verbose_name_plural = 'LDAPGroupUserSearchs'

    def __str__(self):
        return self.ldapgroup.name

    def get_absolute_url(self):
        return reverse("list-connections")






