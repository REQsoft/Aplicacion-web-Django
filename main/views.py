from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .models import *
from .forms import *
from webadmin import settings
import os

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return render(request, 'main/base.html')
    return render(request, '00Login/login.html')

def base_main(request):
    return render(request, "main/base.html")



class AuthenticationUpdateView(UpdateView):
    model = Authentication
    form_class = AuthenticationForm
    template_name = "main/auth_form.html"


class GroupListView(ListView):
    model = Group
    template_name = "main/group_list.html"


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "main/group_form.html"


class LDAPServerUpdateView(UpdateView):
    model = LDAPServer
    form_class = LDAPServerForm
    template_name = "main/auth_ldap_form.html"

    def form_valid(self, form):
        self.object = form.save()
        BASE_DIR = settings.BASE_DIR
        LDAP_settings = open(os.path.join(BASE_DIR, 'webadmin/LDAP_settings.py'), 'w')
        LDAP_settings.write("AUTH_LDAP_SERVER_URI = '"+self.object.AUTH_LDAP_SERVER_URI+"'\n")
        LDAP_settings.write("AUTH_LDAP_BIND_DN = '"+self.object.AUTH_LDAP_BIND_DN+"'\n")
        LDAP_settings.write("AUTH_LDAP_BIND_PASSWORD = '"+self.object.AUTH_LDAP_BIND_PASSWORD+"'\n")
        LDAP_settings.write("AUTH_LDAP_USER_DN_TEMPLATE = '"+self.object.AUTH_LDAP_USER_DN_TEMPLATE+"'\n")
        LDAP_settings.write("AUTH_LDAP_PERMIT_EMPTY_PASSWORD = "+str(self.object.AUTH_LDAP_PERMIT_EMPTY_PASSWORD)+"\n")
        LDAP_settings.write("AUTH_LDAP_GROUP_SEARCH = '"+self.object.AUTH_LDAP_GROUP_SEARCH+"'\n")
        LDAP_settings.write("AUTH_LDAP_USER_SEARCH = '"+self.object.AUTH_LDAP_USER_SEARCH+"'\n")
        LDAP_settings.write("AUTH_LDAP_REQUIRE_GROUP = '"+self.object.AUTH_LDAP_REQUIRE_GROUP+"'\n")
        LDAP_settings.write("AUTH_LDAP_DENY_GROUP = '"+self.object.AUTH_LDAP_DENY_GROUP+"'\n")
        LDAP_settings.close()
        return super(LDAPServerUpdateView, self).form_valid(form)





