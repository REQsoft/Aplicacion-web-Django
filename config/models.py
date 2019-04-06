from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from main.models import DBGroup, LDAPGroup

# Modelos de widgets para mostrar los servicios en la app movil
class Icon(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='icons')

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Icon)
def icon_delete(sender, instance, **kwargs):
    """ Borra los ficheros de los iconos que se eliminan. """
    instance.image.delete(False)

class Folder(models.Model):
    title = models.CharField(max_length=100, unique=True)
    icon = models.ForeignKey(Icon, on_delete="PROTECTED", default=None)
    folder = models.ForeignKey("self", on_delete="PROTECTED", related_name="folders", blank=True, null=True)
    state = models.BooleanField(default=True)
    groups = models.ManyToManyField(DBGroup, blank=True)
    ldapgroups = models.ManyToManyField(LDAPGroup, blank=True)
    description = models.CharField(max_length=300, blank=True)
    type_name = models.CharField(max_length=20, unique=True, blank=True)
    
    def __str__(self):
        return self.title
        
    def save(self):
        super(Folder, self).save()
        if len(self.type_name) == 0:
            self.type_name = "C" + str(self.id)
            self.save()
 
class Colors(models.Model):
    name = models.CharField(max_length=100, unique=True)
    primary = models.CharField(max_length=10)
    light = models.CharField(max_length=10)
    dark = models.CharField(max_length=10)

class Design(models.Model):
    title = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='design')
    favicon = models.ImageField(upload_to='design')
    colors = models.ForeignKey(Colors, on_delete="PROTECTED")

