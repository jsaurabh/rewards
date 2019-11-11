from django.shortcuts import render, redirect
from django.contrib import messages 
from .forms import UsersLoginForm, UsersRegistrationForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import requests, json
#from django import forms
from django.views.generic import View
#from rest_framework.decorators import authentication_classes, permission_classes
#from rest_framework.permissions import IsAuthenticated

LOGIN_URL = "https://webdev.cse.buffalo.edu/rewards/users/auth/login/"
REGISTER_URL = "https://webdev.cse.buffalo.edu/rewards/users/"

class LoginView(View):
    #@authentication_classes((TokenAuthentication, ))
    #permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = UsersLoginForm()
        return render(request, "accounts/login.html", {
            "form":form,
            "title":"Login"
        })

    def post(self, request, *args, **kwargs):
        form = UsersLoginForm(request.POST)
        if form.is_valid():
            post_data = {
                'username':form.cleaned_data.get('username'), 
                'password': form.cleaned_data.get('password')
            }
            response = requests.post(LOGIN_URL, data = post_data)
            token = json.loads(response.text).get('token')
            print(token)
            if token:
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.post(LOGIN_URL, headers = headers, data=post_data)
                return HttpResponseRedirect("/dashboard")
            else:
                messages.error(request, "Error")
        return render(request, "accounts/login.html", {
            "form":form,
            "title":'Login'
        })

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UsersRegistrationForm()
        return render(request, "accounts/register.html", {
            "form":form,
            "title": "Register"
        })
    
    def post(self, request, *args, **kwargs):
        form = UsersRegistrationForm(request.POST)
        if form.is_valid():
            post_data = {
                'username': form.cleaned_data.get("username"),
                'password': form.cleaned_data.get("password"),
                'firstName' : form.cleaned_data.get("password"),
                'lastName': form.cleaned_data.get("lastName"),
                'email': form.cleaned_data.get("email"),
                'phone' : form.cleaned_data.get("phone"),
            }
            response = requests.post(REGISTER_URL, data = post_data)
            token = json.loads(response.text).get('token')
            return HttpResponseRedirect("/accounts/login")
        
        return render(request, "accounts/register.html", {
            "form":form, 
            "title":"Register"
        })

# Create your views here.
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect("/")
#     form = UsersLoginForm(request.POST or None)
#     if form.is_valid():
#         account = form.cleaned_data.get('account_number')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username = account, password = password)
#         login(request, user)
#         return redirect("/dashboard")
#     return render(request, "accounts/login.html",
#     {
#         "form":form,
#         "title": 'Login',
#     })

# def register_view(request):
#     form = UsersRegistrationForm(request.POST or None)
#     if form.is_valid():
        # username = form.cleaned_data.get("username")
        # password = form.cleaned_data.get("password")
        # firstName = form.cleaned_data.get("password")
        # lastName = form.cleaned_data.get("lastName")
        # email = form.cleaned_data.get("email")
        # phone = form.cleaned_data.get("phone")
#         return redirect("/")
#     return render(request, "accounts/register.html",
#     {
#         "form":form,
#         "title":"Register",
#     })

# def logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
        
#         return HttpResponseRedirect("/")
#     return redirect("/")