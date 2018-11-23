from django.urls import path, include
from .views import *

urlpatterns = [
    # Servicio
    path('service/', base_service, name='base-service'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('service/create/', ServiceCreateView.as_view(), name='service-create'),
    path('service/<int:pk>/', service_configure, name='service-configure'), 
    path('service/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service-edit'),   
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
    path('service/<int:pk>/add-element/', add_element, name='add-element'), 

    # Catalogo de objetos perdidos
    path('service/item/<int:pk>/edit', MissingItemUpdateView.as_view(), name='item-edit'),   
    path('service/item/<int:pk>/delete', MissingItemDeleteView.as_view(), name='item-delete'),

    # Directorio de dependencias
    path('service/office/<int:pk>/edit', OfficeUpdateView.as_view(), name='office-edit'),   
    path('service/office/<int:pk>/delete', OfficeDeleteView.as_view(), name='office-delete'),

    # Mapa de Bloques
    path('service/location/<int:pk>/edit', LocationUpdateView.as_view(), name='location-edit'),   
    path('service/location/<int:pk>/delete', LocationDeleteView.as_view(), name='location-delete'),

    # Consulta SQL
    path('service/query/<int:pk>/configure', QueryUpdateView.as_view(), name='query-configure'),
    path(
        'service/query/fields',
        get_fields_service,
        name='fields-service'
    )

]