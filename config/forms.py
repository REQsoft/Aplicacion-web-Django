from django import forms
from .models import *

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["title", "icon", "folder", "state", "dbgroup", "description"]
        labels = {"title": "", "description": "", "dbgroup": "Seleccione los grupos del componente: ", "icon": "Seleccione un icono para el componente:"}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripcion'}),
        }
        error_messages = {"title": {"unique": "Ya existe un componente con ese titulo."}}