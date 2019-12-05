from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import requests, json
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from .forms import BusinessCreationForm, BusinessEditForm, BusinessDeleteForm
from .forms import BusinessCreateWizard, AddCurrencyWizard, AddCatalogWizard
from .users import User
from .tables import NameTable
from rest_framework.parsers import FileUploadParser
from django.contrib import messages
from accounts.forms import UsersLoginForm
import base64
from formtools.wizard.views import SessionWizardView

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
            print(form.cleaned_data)
            post_data = {
                'id': form.cleaned_data.get('business'),
                'name':form.cleaned_data.get('name'), 
                'phone': form.cleaned_data.get('phone'),
                'is_published': form.cleaned_data.get('publish'),
                'url': form.cleaned_data.get('url'),
                'address': form.cleaned_data.get('address'),
                'logo': None
            }
            post_data['phone'] = post_data['phone'].as_e164
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
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 202:
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 200:
                    return HttpResponseRedirect("/dashboard/business")
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "editBusiness.html", {
                    "form" : form
                })

        return render(request, "editBusiness.html", {
                "form": form,
                "title": "Edit Business"
            })

class BusinessDeleteView(View):
    def get(self, request, *args, **kwargs):
        form = BusinessDeleteForm()
        return render(request, "deleteBusiness.html", {
            "form": form,
            "title": "Delete Business"
        })

    def post(self, request, *args, **kwargs):
        form = BusinessDeleteForm(request.POST)
        if form.is_valid():
            #print(form)
            print(form.cleaned_data)
            id = form.cleaned_data.get('business')
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = EDIT_BUSINESS_URL + str(id) + '/'
            USER_URL = USER_READ_URL + str(data.get('user').get('id')) + '/'

            if token:
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response)
                
                user_response = requests.get(USER_URL, headers = headers)
                user_data = json.loads(user_response.text)

                user = User(user_data)
                data['user'] = user_data
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                
                if response.status_code == 400:
                    form.add_error(None, 'Your business could not be deleted')
                    return render(request, "deleteBusiness.html", {
                            "form":form, 
                            "title":"Delete Business"
                            })
                if response.status_code == 405:
                    messages.error(request, "Your business could not be deleted")
                    return render(request, "deleteBusiness.html", {
                            "form":form, 
                            "title":"Delete Business"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your business was successfully deleted")
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 202:
                    messages.info(request, "Your business was successfully deleted")
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 200:
                    messages.info(request, "Your business was successfully deleted")
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 204:
                    return HttpResponseRedirect("/dashboard/business")
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "deleteBusiness.html", {
                    "form" : form
                })

        return render(request, "deleteBusiness.html", {
                "form": form,
                "title": "Delete Business"
            })

class BusinessCreate(View):
    #parser_classes = (FileUploadParser,)
    def get(self, request, *args, **kwargs):
        form = BusinessCreationForm()
        return render(request, "newBusiness.html", {
            "form":form,
            "title":"Add Business"
        })

    def post(self, request, *args, **kwargs):
        form = BusinessCreationForm(request.POST)#, request.FILES)
        #print(request.FILES)
        print(form.is_valid())
        #logo = request.FILES.get('logo')
        if form.is_valid():
            post_data = {
                'name':form.cleaned_data.get('name'), 
                'phone': form.cleaned_data.get('phone'),
                'is_published': True,
                'url': form.cleaned_data.get('url'),
                'address': form.cleaned_data.get('address'),
                #'logo': request.FILES.get('logo')
            }
            
            if post_data['phone']:
                post_data['phone'] = post_data['phone'].as_e164

            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            token = data.get('token')
            print(token)
            id = data.get('user').get('id')
            print(id)
            USER_URL = USER_READ_URL + str(id) + '/'
            print(USER_URL)
            print(CREATE_BUSINESS_URL)
            if token:
                print("In Token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                
                response = requests.post(CREATE_BUSINESS_URL,
                    headers = headers, data = post_data)
                user_response = requests.get(USER_URL, headers = headers)
                print(user_response)
                print(response.text)
                res = json.loads(response.text)
                user_data = json.loads(user_response.text)
                #user = User(user_data)
                data['user'] = user_data
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key][0].title())
                        return render(request, "newBusiness.html", {
                            "form":form, 
                            "title":"Add Business"
                            })
                if response.status_code == 201:
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 202:
                    return HttpResponseRedirect("/dashboard/business")
            else:
                form.add_error(None, "Please ensure you are logged in")
                return redirect("accounts/login")

        return render(request, "newBusiness.html", {
            "form":form,
        })

class FormWizardView(SessionWizardView):
    template_name = "wizard.html"
    form_list = [BusinessCreateWizard, AddCurrencyWizard, AddCatalogWizard]
    
    # def get(self, request, *args, **kwargs):
    #     pass
    def done(self, form_list, **kwargs):
        form_data = process_data(form_list)
        return render(self.request, 'done.html', {
            'form_data': form_data,
        })
    
def process_data(form_list):
    form_data = [form.cleaned_data for form in form_list]
    return form_data

    