import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
AUTH_LDAP_SERVER_URI = 'ldap://192.168.1.17'
AUTH_LDAP_PERMIT_EMPTY_PASSWORD = True
AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
LDAPSearch('ou=People,dc=maxcrc,dc=com', ldap.SCOPE_SUBTREE,'(uid=%(user)s)'),
LDAPSearch('ou=People,dc=maxcrc,dc=com', ldap.SCOPE_SUBTREE,'(uid=%(user)s)'),
LDAPSearch('ou=People,dc=maxcrc,dc=com', ldap.SCOPE_SUBTREE,'(dn=%(user)s)'),)
