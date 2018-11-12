from django import forms
from .models import *

# Formulario para gestionar conexión.
class QueryForm(forms.ModelForm):
    class Meta:

        model = SQLQuery

        fields = [
            "connection",
            "type_name",
            "query_sql",
        ]

        labels = {
            "connection": "Conexión a la base de datos",
            "type_name": "Nombre de clase",
            "query_sql": "Sentencia de datos sql",
        }

        error_messages = {
            "type_name": {"unique": "El nombre de la clase ya existe"},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


# Formulario para gestionar conexión.
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "icon", "kind", "state", "description"]
        error_messages = {"title": {"unique": "El nombre del servicio ya existe."}}


# Formulario para gestionar artículos perdidos.
class MissingItemForm(forms.ModelForm):
    class Meta:
        model = MissingItem
        fields = ["title", "description", "photo"]
        labels = {"title": "", "description": "", "photo": "Foto del objeto: "}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Descripcion'}),
            'photo':forms.FileInput(attrs={'class':'form-control-file'})
        }
        error_messages = {"title": {"unique": "El nombre del objeto ya existe."}}


# Formulario para gestionar directorio de names.
class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office

        fields = ["title", "extension", "phone"]

        labels = {"title": "", "extension": "", "phone": ""}

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la dependencia'}),
            'extension':forms.NumberInput(attrs={'class':'form-control','placeholder':'Extención'}),
            'phone':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número de Telefono'})
        }


# Formulario para gestionar locaclizaciones.
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location

        fields = ["title", "description", "icon", "longitude", "latitude"]

        labels = {"title": "", "description": "", "icon": "", "longitude": "", "latitude": ""}

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la ubicación'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Descripción'}),
            #'icon':forms.FileInput(attrs={'class':'form-control'}),
            'longitude':forms.NumberInput(attrs={'class':'form-control','placeholder':'Longitud'}),
            'latitude':forms.NumberInput(attrs={'class':'form-control','placeholder':'Latitud'})
        }

