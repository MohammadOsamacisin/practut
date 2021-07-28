
from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect
from django.views.generic import ListView, DetailView , TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View, FormView
from django.contrib.auth.decorators import login_required
# Create your views here.
# @login_required
class Dashboard(TemplateView):
    template_name ='customadmin/home.html'

