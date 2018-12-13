# -*- coding: utf-8 -*-
from django import forms
from .models import *

#Formulario para gestionar conexión.
class LDAPServerForm(forms.ModelForm):

    class Meta:

        model = LDAPServer 
        fields = (
            'AUTH_LDAP_SERVER_URI',
            'AUTH_LDAP_BIND_DN',
            'AUTH_LDAP_BIND_PASSWORD',
            'AUTH_LDAP_USER_DN_TEMPLATE',
            'AUTH_LDAP_PERMIT_EMPTY_PASSWORD',
            'AUTH_LDAP_GROUP_SEARCH',
            'AUTH_LDAP_USER_SEARCH',
            'AUTH_LDAP_REQUIRE_GROUP',
            'AUTH_LDAP_DENY_GROUP'
        )

        labels = {
            'AUTH_LDAP_SERVER_URI':'URI servidor',
            'AUTH_LDAP_BIND_DN':'Usuario administrador',
            'AUTH_LDAP_BIND_PASSWORD':'Contraseña',
            'AUTH_LDAP_PERMIT_EMPTY_PASSWORD':'Permitir enlace sin contraseña', 
            'AUTH_LDAP_USER_DN_TEMPLATE':'Plantilla DN de usuario',
            'AUTH_LDAP_USER_SEARCH':'DN usuarios',
            'AUTH_LDAP_GROUP_SEARCH':'DN de grupos',      
            'AUTH_LDAP_REQUIRE_GROUP':'Grupo de usuarios permitidos',
            'AUTH_LDAP_DENY_GROUP':'Grupo de usuarios rechazados' 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'AUTH_LDAP_PERMIT_EMPTY_PASSWORD':
                self.fields[field].widget.attrs.update({'class': 'form-control'})



class AuthenticationForm(forms.ModelForm):

    class Meta:

        model = Authentication 

        fields = [
            'connection',
            'sql_auth',
            'sql_auth_user',
            'description'
        ]

        labels = {
            'connection':'Conexción a base de datos',
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

        
        