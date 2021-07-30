from django.urls import path
from . import views
from .views import Dashboard
from django.contrib.auth import views as auth_views
from django.contrib.auth import login

app_name = 'customadmin'
urlpatterns = [
    path('', Dashboard.as_view(),name ='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]