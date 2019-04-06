from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from connections.models import Connection

class Authentication(models.Model):
    name = models.SlugField(primary_key=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, default=None, null=True)
    sql_auth = models.TextField(blank=True)
    sql_auth_user = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Authentication'
        verbose_name_plural = 'Authentications'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("base-main")


class AuthenticationLDAP(models.Model):
    AUTH_LDAP_SERVER_URI = models.CharField(max_length=100)
    AUTH_LDAP_BIND_DN = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_BIND_PASSWORD = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_USER_DN_TEMPLATE = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_PERMIT_EMPTY_PASSWORD = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'AuthenticationLDAP'
        verbose_name_plural = 'AuthenticationLDAP'

    def __str__(self):
        return 'AuthenticationLDAP'

class LDAPSearchs(models.Model):
    AuthenticationLDAP = models.ForeignKey(AuthenticationLDAP, on_delete=models.CASCADE, related_name='AUTH_LDAP_USER_SEARCH')
    AUTH_LDAP_USER_SEARCH  = models.CharField(max_length=100)

    class Meta:

        verbose_name = 'LDAPSearchs'
        verbose_name_plural = 'LDAPSearchs'

    def __str__(self):
        return self.AUTH_LDAP_USER_SEARCH



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




