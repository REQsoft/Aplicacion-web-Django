from django.contrib import admin
from .models import *

admin.site.register(DBGroup)
admin.site.register(AuthenticationDB)
admin.site.register(AuthenticationLDAP)
admin.site.register(LDAPUserSearch)

# Register your models here.
