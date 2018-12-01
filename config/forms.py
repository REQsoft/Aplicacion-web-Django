from django import forms
from .models import *

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ["title", "icon", "component", "state", "groups", "description"]
        labels = {"title": "", "description": "", "groups": "Seleccione los grupos del componente: ", "icon": "Seleccione un icono para el componente:"}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripcion'}),
        }
        error_messages = {"title": {"unique": "Ya existe un componente con ese titulo."}}