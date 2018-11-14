# -*- coding: utf-8 -*-
from django import forms
from .models import Authentication, Group

#Formulario para gestionar conexión.
class AuthenticationForm(forms.ModelForm):

    class Meta:

        model = Authentication 

        fields = [
            'name',
            'connection',
            'sql_auth',
            'description'
        ]

        labels = {
            'name':'Nombre',
            'connection':'Conexción a base de datos',
            'sql_auth':'Consulta de autenticacion',
            'description':'Descripción'
            
        }

        error_messages = {
            'name': {
                'unique':"El nombre del grupo ya existe.",
            },
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control','required':'required'})


class GroupForm(forms.ModelForm):
    """Form definition for Group."""

    class Meta:

        model = Group 

        fields = [
            'name',
            'authentication',
            'sql_get_user',
        ]

        labels = {
            'name':'Nombre',
            'authentication':'Autenticación',
            'sql_get_user':'Consulta de busqueda',
            
        }

        error_messages = {
            'name': {
                'unique':"El nombre del grupo ya existe.",
            },
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control','required':'required'})

        
        