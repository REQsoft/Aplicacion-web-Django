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

class LDAPServer(models.Model):
    name = models.SlugField(primary_key=True)
    AUTH_LDAP_SERVER_URI = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_BIND_DN = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_BIND_PASSWORD = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_USER_DN_TEMPLATE = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_GROUP_SEARCH = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_PERMIT_EMPTY_PASSWORD = models.BooleanField(default=False)
    AUTH_LDAP_USER_SEARCH  = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_REQUIRE_GROUP = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_DENY_GROUP = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'LDAPServer'
        verbose_name_plural = 'LDAPServers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("base-main")

"""class LDAPSetting(models.Model):
    ldapserver = models.OneToOneField(LDAPServer, on_delete=models.CASCADE)
    AUTH_LDAP_USER_DN_TEMPLATE = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_GROUP_SEARCH = models.CharField(max_length=100, blank=True)
    AUTH_LDAP_PERMIT_EMPTY_PASSWORD = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'LDAPSetting'
        verbose_name_plural = 'LDAPSettings'

    def __str__(self):
        return self.ldapserver.name



class LDAPUserSearch(models.Model):
    authenticationLDAP = models.ForeignKey(LDAPServer, on_delete=models.CASCADE, related_name='AUTH_LDAP_USER_SEARCH')
    AUTH_LDAP_USER_SEARCH  = models.CharField(max_length=100)

    class Meta:

        verbose_name = 'LDAPSearch'
        verbose_name_plural = 'LDAPSearchs'

    def __str__(self):
        return self.AUTH_LDAP_USER_SEARCH


class LDAPRequireGroup(models.Model):
    authenticationLDAP = models.ForeignKey(LDAPServer, on_delete=models.CASCADE, related_name='REQUIRE_GROUP')
    AUTH_LDAP_REQUIRE_GROUP = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'LDAPR'
        verbose_name_plural = 'LDAPRs'

    def __str__(self):
        self.AUTH_LDAP_REQUIRE_GROUP

class LDAPDenyGroup(models.Model):
    authenticationLDAP = models.ForeignKey(LDAPServer, on_delete=models.CASCADE, related_name='DENY_GROUPS')
    AUTH_LDAP_DENY_GROUP = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'LDAPDenyGroup'
        verbose_name_plural = 'LDAPDenyGroups'

    def __str__(self):
        return self.AUTH_LDAP_DENY_GROUP"""




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




