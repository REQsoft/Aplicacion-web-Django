from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import auth
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .models import *
from .forms import *
from webadmin import settings
import os
from django.http import JsonResponse

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



class AuthenticationDBUpdateView(UpdateView):
    model = AuthenticationDB
    form_class = AuthenticationDBForm
    template_name = "main/auth_form.html"

    def get_object(self, queryset=None):
        obj, created = AuthenticationDB.objects.get_or_create(pk='AuthenticationDB')
        return obj


class DBGroupListView(ListView):
    model = DBGroup
    template_name = "main/dbgroup_list.html"

class DBGroupCreateView(CreateView):
    model = DBGroup
    form_class = DBGroupForm
    template_name = "main/DBgroup_form.html"

class LDAPGroupListView(ListView):
    model = LDAPGroup
    template_name = "main/ldapgroup_list.html"

class LDAPGroupCreateView(CreateView):
    model = LDAPGroup
    form_class = LDAPGroupForm
    template_name = "main/ldapgroup_form.html"


class LDAPUserSearchCreateView(CreateView):
    model = LDAPUserSearch
    form_class = LDAPUserSearchForm
    template_name = "main/user_search_form.html"


class LDAPUserSearchUpdateView(UpdateView):
    model = LDAPUserSearch
    form_class = LDAPUserSearchForm
    template_name = "main/user_search_form.html"


class LDAPUserSearchDeleteView(DeleteView):
    model = LDAPUserSearch
    success_url = reverse_lazy("authldap-update")
    

class AuthenticationLDAPUpdateView(UpdateView):
    model = AuthenticationLDAP
    form_class = AuthenticationLDAPForm
    template_name = "main/auth_ldap_form.html"

    def get_object(self, queryset=None):
        obj, created = AuthenticationLDAP.objects.get_or_create(pk='AuthenticationLDAP')
        return obj

    def get_context_data(self, **kwargs):
        context = super(AuthenticationLDAPUpdateView, self).get_context_data(**kwargs)
        try:
            context['USER_SEARCH'] = LDAPUserSearch.objects.all()
        except:
            pass
        return context


    def form_valid(self, form):
        self.object = form.save()
        
        BASE_DIR = settings.BASE_DIR
        ldap_settings = open(os.path.join(BASE_DIR, 'webadmin/ldap_settings.py'), 'w')


        ldap_settings.write("import ldap\n")
        ldap_settings.write("from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion\n")

        ldap_settings.write("AUTH_LDAP_SERVER_URI = '"+self.object.SERVER_URI+"'\n")
        ldap_settings.write("AUTH_LDAP_PERMIT_EMPTY_PASSWORD = "+str(self.object.PERMIT_EMPTY_PASSWORD)+"\n")

        if self.object.authentication == '1':
            ldap_settings.write("AUTH_LDAP_USER_DN_TEMPLATE = '"+self.object.USER_DN_TEMPLATE+"'\n")
        else:
            LDAPSearchs = ''
            for user_search in LDAPUserSearch.objects.all():
                LDAPSearchs += "\nLDAPSearch('"+ user_search.USER_SEARCH +"', ldap.SCOPE_SUBTREE,'("+user_search.filter_attr+"=%(user)s)'),"

            ldap_settings.write("AUTH_LDAP_USER_SEARCH = LDAPSearchUnion("+LDAPSearchs+")\n")

        ldap_settings.close()

        return super(AuthenticationLDAPUpdateView, self).form_valid(form)

def set_backend_setting_db_auth(request):
    BASE_DIR = settings.BASE_DIR

    auth_backend_setting = open(os.path.join(BASE_DIR, 'webadmin/authentication_backend_settings.py'), 'w')
    auth_backend_setting.write("authentication_backend = 'webadmin.backends.CustomBackend'")
    auth_backend_setting.close()
    context =  {"object":True}

    return JsonResponse(context) 

def set_backend_setting_ldap_auth(request):
    BASE_DIR = settings.BASE_DIR

    auth_backend_setting = open(os.path.join(BASE_DIR, 'webadmin/authentication_backend_settings.py'), 'w')
    auth_backend_setting.write("authentication_backend = 'webadmin.backends.LDAPBackend'")
    auth_backend_setting.close()
    context =  {"object":True}

    return JsonResponse(context) 





