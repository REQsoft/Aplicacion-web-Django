from django.urls import path
from .views import *

urlpatterns = [
    path('components/<int:pk>/', component_configure, name='component-list'),
    path('component/create/', ComponentCreateView.as_view(), name='component-create'),
    path('component/<int:pk>/edit/', ComponentUpdateView.as_view(), name='component-edit'),   
    path('component/<int:pk>/delete/', ComponentDeleteView.as_view(), name='component-delete'),
]