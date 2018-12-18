# -*- coding: utf-8 -*-
from django import forms
from .models import *

#Formulario para gestionar conexión.
class AuthenticationLDAPForm(forms.ModelForm):

    class Meta:

        model = AuthenticationLDAP 
        fields = (
            'SERVER_URI',
            'USER_DN_TEMPLATE',
            'PERMIT_EMPTY_PASSWORD',
            'GROUP_SEARCH',
            'REQUIRE_GROUP',
            'DENY_GROUP',
            'authentication',
        )

        labels = {
            'SERVER_URI':'URI servidor',
            'PERMIT_EMPTY_PASSWORD':'Permitir enlace sin contraseña', 
            'USER_DN_TEMPLATE':'Plantilla DN de usuario',
            'GROUP_SEARCH':'DN de grupos',      
            'REQUIRE_GROUP':'Grupo de usuarios permitidos',
            'DENY_GROUP':'Grupo de usuarios rechazados',
            'authentication':'Autenticación'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'PERMIT_EMPTY_PASSWORD':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class LDAPUserSearchForm(forms.ModelForm):

    class Meta:
        model = LDAPUserSearch
        fields = (
            'USER_SEARCH',
            'filter_attr',
            )

        labels = {
            'USER_SEARCH':'DN base del grupo',
            'filter_attr':'Atributo de filtro de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AuthenticationDBForm(forms.ModelForm):

    class Meta:

        model = AuthenticationDB 

        fields = [
            'connection',
            'sql_auth',
            'sql_auth_user',
            'description'
        ]

        labels = {
            'connection':'Conexión a base de datos',
            'sql_auth':'Consulta de autenticación básica',
            'sql_auth_user':'Consulta de autenticación por token',
            'description':'Descripción'            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class GroupForm(forms.ModelForm):
    """Form definition for Group."""

    class Meta:

        model = Group 

        fields = [
            'connection',
            'name',
            'sql_get_user',
        ]

        labels = {
            'connection':'Conexion a base de datos',
            'name':'Nombre',
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

        
        