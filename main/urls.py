from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('main', base_main, name='base-main'),
    path('authdb/update', AuthenticationDBUpdateView.as_view(), name='authdb-update'),
    path('groups/create', GroupCreateView.as_view(), name='group-create'),
    path('groups/list', GroupListView.as_view(), name='group-list'),
    path('authldap/update', AuthenticationLDAPUpdateView.as_view(), name='authldap-update'),
    path('search/user/create', LDAPUserSearchCreateView.as_view(), name='search-user-create'),
    path('search/user/<int:pk>/update', LDAPUserSearchUpdateView.as_view(), name='search-user-update'),
    path('search/user/<int:pk>/delete', LDAPUserSearchDeleteView.as_view(), name='search-user-remove'),
    path('authldap/update/backend', set_backend_setting_ldap_auth, name='auth-ldap-backend-set'),
    path('authdb/update/backend', set_backend_setting_db_auth, name='authdb-backend-set'),
]
