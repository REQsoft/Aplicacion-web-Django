from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .models import Group, Authentication
from .forms import GroupForm, AuthenticationForm

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
            return render(request, '00Login/base.html')
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


