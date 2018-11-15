from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('main', base_main, name='base-main'),
    path('auth/create', AuthenticationCreateView.as_view(), name='auth-create'),
    path('groups/create', GroupCreateView.as_view(), name='group-create'),
]
