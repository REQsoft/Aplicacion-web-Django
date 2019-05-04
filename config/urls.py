from django.urls import path
from .views import *

urlpatterns = [
    path('components/<int:pk>/', component_list, name='component-list'),
    path('component/create/', FolderCreateView.as_view(), name='folder-create'),
    path('component/<int:parent>/create/', FolderCreateView.as_view(), name='folder-create'),
    path('component/<int:pk>/<int:parent>/edit/', FolderUpdateView.as_view(), name='folder-edit'),
    path('component/<int:pk>/edit/', FolderUpdateView.as_view(), name='folder-edit'),  
    path('component/<int:pk>/delete/', FolderDeleteView.as_view(), name='folder-delete'),
    # path('config/<color>/color.css', color_css),
]