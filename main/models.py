from django.db import models
from django.contrib.auth.models import User
from app_connection.models import Connection

class Authentication(models.Model):
    name = models.CharField(max_length=20, unique=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    sql_auth = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Authentication'
        verbose_name_plural = 'Authentications'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("list-connections")


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    authentication = models.ForeignKey(Authentication, on_delete=models.CASCADE)
    sql_get_user = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("list-connections")




