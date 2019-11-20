from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import UsersLoginForm, UsersRegistrationForm
from django.http import HttpResponseRedirect
import requests, json
from django.views.generic import View
from dashboard.users import User
from django.contrib.auth.models import User as U

#API routes
LOGIN_URL = "https://webdev.cse.buffalo.edu/rewards/users/auth/login/"
REGISTER_URL = "https://webdev.cse.buffalo.edu/rewards/users/"

class LoginView(View):
    def get(self, request, *args, **kwargs):
        print(request)
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
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(json.loads(response.text), f, indent=4)

            user = User(json.loads(response.text))
            token = json.loads(response.text).get('token')
            print(token)
            if token:
                try:
                    user = authenticate(username = post_data['username'], password = post_data['password'])
                    login(request, user)
                    return HttpResponseRedirect("/dashboard")
                except:
                    messages.error(request, "Unable to log in with provided credentials")
                    return render(request, "accounts/login.html", {
                        "form":form
                        })
            else:
                messages.error(request, "Please enter valid account data")
                return render(request, "accounts/login.html", {
                        "form":form
                        })
        return render(request, "accounts/login.html", {
            "form":form,
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
            res = json.loads(response.text)
            if response.status_code == 400:
                for key in res:
                    messages.error(request, res[key][0].capitalize())
                return render(request, "accounts/register.html", {
                    "form":form, 
                    "title":"Register"
        })
            if response.status_code == 200:
                try:
                    userobj = U.objects.create_superuser(post_data['username'], post_data['email'], post_data['password'])
                    token = json.loads(response.text).get('token')
                    print(res)
                    print(token)
                    return HttpResponseRedirect("/accounts/login")
                except:
                    print("Superuser can't be created")
                    
        return render(request, "accounts/register.html", {
            "form":form, 
            "title":"Register"
        })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        
        return HttpResponseRedirect("/")
    return redirect("/")