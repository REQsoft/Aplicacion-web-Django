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
            'table_users',
            'field_username',
            'field_password'
        ]

        labels = {
            'connection':'Conexión a base de datos',
            'table_users':'Tabla de usuarios',
            'field_username':'Campo para nombre de usuario',
            'field_password':'Campo para contraseña'            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class DBGroupForm(forms.ModelForm):
    """Form definition for Group."""

    class Meta:

        model = DBGroup 

        fields = [
            'name',
            'sql_check_user',
        ]

        labels = {
            'name':'Nombre',
            'sql_check_user':'Plantilla sql de usuario',
            
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

        
class LDAPGroupForm(forms.ModelForm):
    """Form definition for Group."""

    class Meta:

        model = LDAPGroup 

        fields = [
            'name',
            'type_bind',
            'USER_DN_TEMPLATE'
        ]

        labels = {
            'name':'Nombre del grupo',
            'type_bind':'Tipe de enlace de usuario',
            'USER_DN_TEMPLATE':'PLantilla DN de usuario',
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
        
class LDAPGroupUserSearchForm(forms.ModelForm):

    class Meta:
        model = LDAPGroupUserSearch
        fields = (
            'dn_base',
            'filter_attr',
            )

        labels = {
            'dn_base':'DN base del grupo',
            'filter_attr':'Atributo de filtro de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
