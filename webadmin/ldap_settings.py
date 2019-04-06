import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
AUTH_LDAP_SERVER_URI = 'ldap://192.168.1.17'
AUTH_LDAP_PERMIT_EMPTY_PASSWORD = False
AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
LDAPSearch('ASDFA', ldap.SCOPE_SUBTREE,'(XADF=%(user)s)'),
LDAPSearch('ASDFA', ldap.SCOPE_SUBTREE,'(ASDF=%(user)s)'),
LDAPSearch('FFF', ldap.SCOPE_SUBTREE,'(RER=%(user)s)'),
LDAPSearch('123', ldap.SCOPE_SUBTREE,'(cvcd=%(user)s)'),)
