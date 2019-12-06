from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import requests, json
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from .forms import BusinessCreationForm, BusinessEditForm, BusinessDeleteForm
from .forms import BusinessCreateWizard, AddCurrencyWizard
from .users import User
from .tables import NameTable
from rest_framework.parsers import FileUploadParser
from accounts.forms import UsersLoginForm
import base64
from formtools.wizard.views import SessionWizardView

## API routes
CREATE_BUSINESS_URL = EDIT_BUSINESS_URL = "https://webdev.cse.buffalo.edu/rewards/programs/businesses/"
USER_READ_URL = "https://webdev.cse.buffalo.edu/rewards/users/"
CAMPAIGN_URL = "https://webdev.cse.buffalo.edu/rewards/programs/campaigns/"

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
            try:
                businesses = res.get('employee_of')
            except:
                businesses = []
            table = NameTable(businesses)
            return render(request, 'business.html', {
            "title": "UB Loyalty | Business",
            "table" : table 
        })
        
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
        form = BusinessEditForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            logo = form.cleaned_data.get('logo')
            post_data = {
                'id': form.cleaned_data.get('business'),
                'name':form.cleaned_data.get('name'), 
                'phone': form.cleaned_data.get('phone'),
                'is_published': form.cleaned_data.get('publish'),
                'url': form.cleaned_data.get('url'),
                'address': form.cleaned_data.get('address'),
            }
            if post_data['phone']:
                post_data['phone'] = post_data['phone'].as_e164
            #post_data['phone'] = post_data['phone'].as_e164
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = EDIT_BUSINESS_URL + str(post_data['id']) + '/'
            USER_URL = USER_READ_URL + str(data.get('user').get('id')) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.put(EDIT_URL, headers = headers, data = post_data, files = {"logo": logo})
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
                        form.add_error(None, res[key][0].capitalize())
                        return render(request, "editBusiness.html", {
                            "form":form, 
                            "title":"Edit Business"
                            })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, res[key][0].capitalize())
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
                    form.add_error(None, "Your business could not be deleted")
                    return render(request, "deleteBusiness.html", {
                            "form":form, 
                            "title":"Delete Business"
                            })
                if response.status_code == 201:
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 202:
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 200:
                    return HttpResponseRedirect("/dashboard/business")
                if response.status_code == 204:
                    return HttpResponseRedirect("/dashboard/business")
            else:
                form.add_error(None, "Your request could not be completed")
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
        form = BusinessCreationForm(request.POST, request.FILES)
        #print(request.FILES)
        print(form.is_valid())
        logo = form.cleaned_data.get('logo')
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
                    headers = headers, data = post_data, files = {"logo": logo})
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
    form_list = [BusinessCreateWizard, AddCurrencyWizard]
    
    # def get(self, request, *args, **kwargs):
    #     pass
    def done(self, form_list, **kwargs):
        form_data = process_data(form_list)
        #print(form_data)

        with open('data.json') as f:
            data = json.loads(f.read())

        token = data.get('token')
        id = data.get('user').get('id')

        if token:
            tokenh = f"Token {token}"
            headers = {"Authorization": tokenh}

        USER_URL = USER_READ_URL + str(id) + '/'

        #######
        ## Process first step of the form

        if form_data[0].get('phone'):
            form_data[0]['phone'] = form_data[0].get('phone').as_e164

        # logo = form_data[0].cleaned_data.get('logo')

        response = requests.post(CREATE_BUSINESS_URL,
                    headers = headers, data = form_data[0])
        user_response = requests.get(USER_URL, headers = headers)
        #print(response)
        res = json.loads(response.text)
        print(res)
        user_data = json.loads(user_response.text)
        data['user'] = user_data

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        #######
        ## Process second step of the form

        biz = res.get('id')
        print(biz)

        r = requests.get(url = "https://young-ravine-99554.herokuapp.com/rewards/currency")

        with open('currency.json', 'r') as f:
            data = json.loads(f.read())

        for item in data['currency']: 
            if item['business'] == biz:
                id = item['id']

        form_data[1]['business'] = biz
        form_data[1]['currency'] = id
        print(form_data[1])

        response = requests.post(CAMPAIGN_URL, headers = headers, data = form_data[1])
        print(response, response.text)

        return render(self.request, 'index.html')
    
def process_data(form_list):
    form_data = [form.cleaned_data for form in form_list]
    return form_data

    