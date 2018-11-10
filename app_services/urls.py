from django.urls import path, include
from .views import *

urlpatterns = [
    # Servicio
    path('services/', base_service, name='base-service'),
    path('services/list', ServiceListView.as_view(), name='service-list'),
    path('services/create/', ServiceCreateView.as_view(), name='service-create'),
    path('services/edit/<int:service_id>/', ServiceUpdateView.as_view(), name='service-edit'),   
    path('services/delete/<int:service_id>/', ServiceDeleteView.as_view(), name='service-delete'),
    path('services/<int:service_id>/', service_configure, name='service-configure'), 
    path('services/<int:service_id>/add_element/', add_element, name='add-element'), 

    # Catalogo de objetos perdidos
    #path('services/items/<int:service_id>/create', item_create, name='item-create'),
    path('services/items/<int:pk>/edit', MissingItemUpdateView.as_view(), name='item-edit'),   
    path('services/items/<int:pk>/delete', MissingItemDeleteView.as_view(), name='item-delete'),

    # Directorio de dependencias
    #path('services/offices/<int:service_id>/create', office_create, name='office-create'),
    path('services/offices/<int:pk>/edit', OfficeUpdateView.as_view(), name='office-edit'),   
    path('services/offices/<int:pk>/delete', OfficeDeleteView.as_view(), name='office-delete'),

    # Mapa de Bloques
    #path('services/locations/<int:service_id>/create', location_create, name='location-create'),
    path('services/locations/<int:pk>/edit', LocationUpdateView.as_view(), name='location-edit'),   
    path('services/locations/<int:pk>/delete', LocationDeleteView.as_view(), name='location-delete'),

    # Consulta SQL
    path('services/query/<int:service_id>/configure', QueryCreateView.as_view(), name='query-configure'),
    path(
        'services/query/fields',
        get_fields_service,
        name='fields-service'
    )

]