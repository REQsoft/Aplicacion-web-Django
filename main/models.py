from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from connections.models import Connection

class Authentication(models.Model):
    name = models.SlugField(primary_key=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, default=None, null=True)
    sql_auth = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Authentication'
        verbose_name_plural = 'Authentications'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("base-main")


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




