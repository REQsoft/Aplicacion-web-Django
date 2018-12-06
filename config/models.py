from django.db import models
from main.models import Group

# Modelos de widgets para mostrar los servicios en la app movil
class Icon(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='icons')

    def __str__(self):
        return self.title

class Folder(models.Model):
    title = models.CharField(max_length=100, unique=True)
    icon = models.ForeignKey(Icon, on_delete="PROTECTED", default=None)
    folder = models.ForeignKey("self", on_delete="PROTECTED", related_name="folders", blank=True, null=True)
    state = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, blank=True)
    description = models.CharField(max_length=300, blank=True)
    type_name = models.CharField(max_length=20, unique=True, blank=True)
    
    
    def __str__(self):
        return self.title
        
    def save(self):
        super(Folder, self).save()
        if len(self.type_name) == 0:
            self.type_name = "C" + str(self.id)
            self.save()
