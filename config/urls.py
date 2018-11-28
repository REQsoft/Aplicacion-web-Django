from django.urls import path
from .views import *

urlpatterns = [
    path('config/', base_config, name='config'),
    path('components/', ComponentListView.as_view(), name='component-list'),
    path('components/<int:pk>/', component_configure, name='component-configure'),
]