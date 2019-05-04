from django import forms
from .models import *

# Formulario para gestionar conexión.
class QueryForm(forms.ModelForm):
    class Meta:

        model = SQLQuery

        fields = [
            "connection",
            "query_sql",        ]

        labels = {
            "connection": "Conexión a base de datos",
            "query_sql": "Sentencia de datos sql",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

class FieldForm(forms.ModelForm):
    class Meta:

        model = Field

        fields = [
            'name',
            'label',
            'visible'
        ]

        labels = {
            'name':'Nombre',
            'label':'Nobre de etiqueta',
            'visible':'visible'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

# Formulario para gestionar conexión.
class ServiceForm(forms.ModelForm):
    icon_label_message = 'Icono'
    folder_label_message = 'Ubicacion'
    theme_label_message = 'Plantilla'
    source_label_message = 'Tipo'

    class Meta:
        model = Service
        fields = ["title", "icon", "theme", "folder", "groups", "source", "description"]
        labels = {"title": "", "description": "", "theme": "", "icon": ""}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo','required':''}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripcion'}),
            'groups':forms.SelectMultiple(attrs={'class':'chosen-select','data-placeholder':'Permisos','multiple':''}),
            'icon':forms.Select(attrs={'class':'chosen-select','data-placeholder':'Icono','required':''}),
            'theme':forms.Select(attrs={'class':'chosen-select','data-placeholder':'Plantilla','required':''}),
            'source':forms.Select(attrs={'class':'chosen-select','data-placeholder':'Tipo','required':''}),
            'folder':forms.Select(attrs={'class':'chosen-select','data-placeholder':'Ubicacion','required':''}),

        }
        error_messages = {"title": {"unique": "Ya existe un servicio con ese titulo."}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon'].empty_label = self.icon_label_message
        self.fields['theme'].empty_label = self.theme_label_message
        self.fields['source'].empty_label = self.source_label_message
        self.fields['folder'].empty_label = self.folder_label_message

# Formulario para gestionar artículos perdidos.
class MissingItemForm(forms.ModelForm):
    class Meta:
        model = MissingItem
        fields = ["title", "description", "photo"]
        labels = {"title": "", "description": "", "photo": "Foto del objeto: "}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripcion'}),
            'photo':forms.FileInput(attrs={'class':'form-control-file'})
        }
        error_messages = {"title": {"unique": "Ya existe un objeto con ese titulo."}}


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

        error_messages = {"title": {"unique": "Ya existe una dependencia con ese nombre."}}

# Formulario para gestionar locaclizaciones.
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location

        fields = ["title", "description", "icon", "longitude", "latitude"]

        labels = {"title": "", "description": "", "icon": "", "longitude": "", "latitude": ""}

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la ubicación'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Descripción'}),
            #'icon':forms.FileInput(attrs={'class':'form-control'}),
            'longitude':forms.NumberInput(attrs={'class':'form-control','placeholder':'Longitud'}),
            'latitude':forms.NumberInput(attrs={'class':'form-control','placeholder':'Latitud'})
        }

        error_messages = {"title": {"unique": "Ya existe una ubicacion con ese titulo."}}

