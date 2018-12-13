from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(Authentication)
admin.site.register(LDAPServer)

# Register your models here.
