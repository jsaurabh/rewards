from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import requests, json
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from .forms import BusinessCreationForm, BusinessEditForm
from .users import User
from .tables import NameTable

from django.contrib import messages
from accounts.forms import UsersLoginForm

## API routes
CREATE_BUSINESS_URL = EDIT_BUSINESS_URL = "https://webdev.cse.buffalo.edu/rewards/programs/businesses/"
USER_READ_URL = "https://webdev.cse.buffalo.edu/rewards/users/"

class DashView(TemplateView):
    template_name = 'index.html'

class BusinessView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
                data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"
        id = data.get('user').get('id')
        USER_URL = USER_READ_URL + str(id) + '/'
        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(USER_URL, headers = headers)
            res = json.loads(user_response.text)
            data['user'] = res
            businesses = res.get('employee_of')
            table = NameTable(businesses)
            return render(request, 'business.html', {
            "title": "UB Loyalty | Business",
            "table" : table 
        })

        # return render(request, 'business.html', {
        #     "title": "UB Loyalty | Business", 
        # })
    def post(self, request, *args, **kwargs):
        pass

class BusinessEditView(View):
    def get(self, request, *args, **kwargs):
        form = BusinessEditForm()
        return render(request, "editBusiness.html", {
            "form": form,
            "title": "Edit Business"
        })

    def post(self, request, *args, **kwargs):
        form = BusinessEditForm(request.POST)
        if form.is_valid():
            print("valid")
            post_data = {
                'id': form.cleaned_data.get('id'),
                'name':form.cleaned_data.get('name'), 
                'phone': form.cleaned_data.get('phone'),
                'is_published': True,
                'url': form.cleaned_data.get('url'),
                'address': form.cleaned_data.get('address'),
                'logo': None
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = EDIT_BUSINESS_URL + str(post_data['id']) + '/'
            USER_URL = USER_READ_URL + str(data.get('user').get('id')) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                res = json.loads(response.text)
                print(res)
                user_response = requests.get(USER_URL, headers = headers)
                user_data = json.loads(user_response.text)
                print(user_data)
                print(user_response)
                user = User(user_data)
                data['user'] = user_data
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0].capitalize())
                        return render(request, "editBusiness.html", {
                            "form":form, 
                            "title":"Edit Business"
                            })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, res[key][0].capitalize())
                        return render(request, "editBusiness.html", {
                            "form":form, 
                            "title":"Edit Business"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your business was successfully edited")
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 202:
                    messages.info(request, "Your business was successfully edited")
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 200:
                    messages.info(request, "Your business was successfully edited")
                    return HttpResponseRedirect("/dashboard/business")
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "editBusiness.html", {
                    "form" : form
                })

        return render(request, "editBusiness.html", {
                "form": form,
                "title": "Edit Business"
            })

class BusinessCreate(View):
    def get(self, request, *args, **kwargs):
        form = BusinessCreationForm()
        return render(request, "newBusiness.html", {
            "form":form,
            "title":"Add Business"
        })

    def post(self, request, *args, **kwargs):
        form = BusinessCreationForm(request.POST)
        if form.is_valid():
            post_data = {
                'name':form.cleaned_data.get('name'), 
                'phone': form.cleaned_data.get('phone'),
                'is_published': True,
                'url': form.cleaned_data.get('url'),
                'address': form.cleaned_data.get('address'),
                'logo': None
            }
           
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            token = data.get('token')
            id = data.get('user').get('id')
            USER_URL = USER_READ_URL + str(id) + '/'

            if token:
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.post(CREATE_BUSINESS_URL, headers = headers, data = post_data)
                user_response = requests.get(USER_URL, headers = headers)
                print(user_response)
                print(response)
                res = json.loads(response.text)
                user_data = json.loads(user_response.text)
                user = User(user_data)
                data['user'] = user_data
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0].capitalize())
                        return render(request, "newBusiness.html", {
                            "form":form, 
                            "title":"Add Business"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your business was successfully added")
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 202:
                    messages.info(request, "Your business was successfully added")
                    return HttpResponseRedirect("/dashboard/business")
            else:
                messages.error(request, "Please ensure you are logged in")
                return redirect("accounts/login")

        return render(request, "newBusiness.html", {
            "form":form,
        })