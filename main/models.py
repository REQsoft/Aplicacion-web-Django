from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from connections.models import Connection

class AuthenticationDB(models.Model):
    name = models.SlugField(primary_key=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, default=None, null=True)
    sql_auth = models.TextField(blank=True)
    sql_auth_user = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'AuthenticationDB'
        verbose_name_plural = 'AuthenticationDB'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("authdb-update")

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

    class Meta:
        verbose_name = 'AuthenticationLDAP'
        verbose_name_plural = 'AuthenticationLDAP'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("authldap-update")


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


class Group(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, unique=True)
    sql_get_user = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("list-connections")




