from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from . forms import SignUpForm
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/products')
    else:
        form = SignUpForm()
    context = {}
    # form = UserCreationForm(request.POST or None)
    # if request.method == "POST":
    #     if form.is_valid():
    #         user = form.save()
    #         # import pdb
    #         # pdb.set_trace()
    #         login(request,user)
    #         return render(request,'/products')
    context['form']=form
    return render(request,'registration/sign_up.html',context)