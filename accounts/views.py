from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UsersRegistrationForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        account = form.cleaned_data.get('account_number')
        password = form.cleaned_data.get('password')
        user = authenticate(username = account, password = password)
        login(request, user)
        return redirect("/dashboard")
    return render(request, "accounts/login.html",
    {
        "form":form,
        "title": 'Login',
    })

def register_view(request):
    form = UsersRegistrationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        firstName = form.cleaned_data.get("password")
        lastName = form.cleaned_data.get("lastName")
        email = form.cleaned_data.get("email")
        phone = form.cleaned_data.get("phone")
        return redirect("/")
    return render(request, "accounts/register.html",
    {
        "form":form,
        "title":"Register",
    })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        
        return HttpResponseRedirect("/")
    return redirect("/")