from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('main', base_main, name='base-main'),

    path('authdb/update', AuthenticationDBUpdateView.as_view(), name='authdb-update'),
    path('dbgroup/create', DBGroupCreateView.as_view(), name='dbgroup-create'),
    path('dbgroups/list', DBGroupListView.as_view(), name='dbgroup-list'),

    path('authldap/update', AuthenticationLDAPUpdateView.as_view(), name='authldap-update'),
    path('ldapgroup/create', LDAPGroupCreateView.as_view(), name='ldapgroup-create'), 
    path('ldapgroups/list', LDAPGroupListView.as_view(), name='ldapgroup-list'),
  
    path('search/user/create', LDAPUserSearchCreateView.as_view(), name='search-user-create'),
    path('search/user/<int:pk>/update', LDAPUserSearchUpdateView.as_view(), name='search-user-update'),
    path('search/user/<int:pk>/delete', LDAPUserSearchDeleteView.as_view(), name='search-user-remove'),
    
    path('authldap/update/backend', set_backend_setting_ldap_auth, name='auth-ldap-backend-set'),
    path('authdb/update/backend', set_backend_setting_db_auth, name='authdb-backend-set'),
]
