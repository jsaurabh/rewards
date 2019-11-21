from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import UsersLoginForm, UsersRegistrationForm
from django.http import HttpResponseRedirect
import requests, json
from django.views.generic import View
from dashboard.users import User
from django.contrib.auth.models import User as U
import phonenumbers

#API routes
LOGIN_URL = "https://webdev.cse.buffalo.edu/rewards/users/auth/login/"
REGISTER_URL = "https://webdev.cse.buffalo.edu/rewards/users/"

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard")
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

            #user = User(json.loads(response.text))
            token = json.loads(response.text).get('token')
            print(token)
            if token:
                try:
                    user = authenticate(username = post_data['username'], password = post_data['password'])
                    login(request, user)
                    return HttpResponseRedirect("/dashboard")
                except:
                    print("Unable to log user with provided credentials")
                    form.add_error(None, "Unable to log in with given credentials")
                    #messages.error(request, "Unable to log in with provided credentials")
                    return render(request, "accounts/login.html", {
                        "form":form
                        })
            else:
                form.add_error(None, "Your account could not be found. Please try again")

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
            "form": form,
            "title": "Register"
        })
    
    def post(self, request, *args, **kwargs):
        form = UsersRegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            if phone:
                number = phone.as_e164
            else:
                number = ""
            post_data = {
                'username': form.cleaned_data.get("username"),
                'password': form.cleaned_data.get("password"),
                'firstName' : form.cleaned_data.get("password"),
                'lastName': form.cleaned_data.get("lastName"),
                'email': form.cleaned_data.get("email"),
                'phone' : number
            } 
            response = requests.post(REGISTER_URL, data = post_data)
            res = json.loads(response.text)
            print(response.status_code)
            print(res)
            if response.status_code == 400:
                for key in res:
                    for val in res[key]:
                        form.add_error(key, val.capitalize())
                        #messages.error(request, val.capitalize())
                return render(request, "accounts/register.html", {
                    "form":form, 
                    "title":"Register"
                })
            if response.status_code == 200:
                try:
                    userobj = U.objects.create_superuser(post_data['username'], post_data['email'], post_data['password'])
                except:
                    form.add_error(None, "User could not be created")
                    print("Superuser can't be created")
                token = res.get('token')
                if token:
                    try:
                        user = authenticate(username = post_data['username'], password = post_data['password'])
                        login(request, user)
                        return HttpResponseRedirect("/dashboard")
                    except:
                        print("Unable to log user in with provided credentials")
                        messages.error(request, "Unable to log in with provided credentials")
                        return render(request, "accounts/login.html", {
                        "form":form
                        })
                    
        return render(request, "accounts/register.html", {
            "form":form, 
            "title":"Register"
        })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        
        return HttpResponseRedirect("/")
    return redirect("/")