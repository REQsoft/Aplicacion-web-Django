from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('main', base_main, name='base-main'),
    path('auth/<slug:pk>/update', AuthenticationUpdateView.as_view(), name='auth-update'),
    path('groups/create', GroupCreateView.as_view(), name='group-create'),
    path('groups/list', GroupListView.as_view(), name='group-list'),
    path('ldap/<slug:pk>/update', LDAPServerUpdateView.as_view(), name='ldap-update'),
]
