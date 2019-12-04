from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import AddCampaignForm, DeleteCampaignForm, EditCampaignForm
from .forms import AddCurrencyForm, EditCurrencyForm, DeleteCurrencyForm
from .forms import AddAccRulesForm, EditAccRulesForm, DeleteAccRulesForm
from .forms import AddRedRulesForm, EditRedRulesForm, DeleteRedRulesForm
from django.http import HttpResponseRedirect
import requests, json
from django.views.generic import View
from dashboard.users import User
from .tables import CurrencyTable, CampaignTable, AccRulesTable, RedRulesTable
from ast import literal_eval

# API routes
CURRENCY_URL = "https://webdev.cse.buffalo.edu/rewards/programs/currencies/"
CAMPAIGN_URL = "https://webdev.cse.buffalo.edu/rewards/programs/campaigns/"
ACC_RULES = "https://webdev.cse.buffalo.edu/rewards/rewards/accumulation-rules/"
RED_RULES = "https://webdev.cse.buffalo.edu/rewards/rewards/redemption-rules/"

# Create your views here.
class RewardsView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        
        with open('currency.json', 'r') as f:
            curr = json.loads(f.read())

        token = data.get('token')
        biz = data.get('user').get('employee_of')[0].get('id')
        tokenh = f"Token {token}"

        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(CAMPAIGN_URL, headers = headers)
            res = json.loads(user_response.text)
            campaigns = []
            #print(res)
            for idx, _ in enumerate(res):
                if res[idx].get('business') == biz:
                    d = {
                    'id' : res[idx].get('id'),
                    'name': res[idx].get('name'),
                    'start': res[idx].get('starts_at'),
                    'end' : res[idx].get('ends_at'),
                    'expiry': res[idx].get('points_expire_after'),
                    'business': data.get('user').get('employee_of')[0].get('name'),
                    'currency': curr["currency"][0].get('label')}
                    campaigns.append(d)
            
            with open('campaigns.json', 'w', encoding = 'utf-8') as f:
                json.dump(campaigns, f, indent= 4)
            print(campaigns)
            table = CampaignTable(campaigns)
            return render(request, 'rewards/rewards.html', {
            "title": "UB Loyalty | Currency",
            "table" : table 
        })

    def post(self, request, *args, **kwargs):
        pass

class RulesView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"

        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(ACC_RULES, headers = headers)
            res = json.loads(user_response.text)
            accRules = []
            #print(res)
            # for idx, _ in enumerate(res):
            #     d = {
            #         'id' : res[idx].get('id'),
            #         'value': res[idx].get('value'),
            #         'campaign': res[idx].get('campaign'),
            #         'category' : res[idx].get('category'),
            #         'item': res[idx].get('item'),
            #     }
            #     accRules.append(d)
            
            # table = AccRulesTable(accRules)
            return render(request, 'rewards/Rules.html', {
            "title": "UB Loyalty | Currency"
            # "table" : table 
        })

class DeleteCampaign(View):
    def get(self, request, *args, **kwargs):
        form = DeleteCampaignForm()
        return render(request, "rewards/deleteCampaign.html", {
            "form": form,
            "title": "UB Loyalty | Delete Campaign"
        }) 

    def post(self, request, *args, **kwargs):
        form = DeleteCampaignForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('choose_campaign')

            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CAMPAIGN_URL + str(id) + '/'
            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response.status_code)
                # print(response)
                # res = json.loads(response.text)
                # print(res)
                
                if response.status_code == 404:
                    messages.error(request, "Please check the currency exists")
                    return render(request, "rewards/deleteCampaign.html", {
                        "form": form,
                        "title": "Delete Campaign"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please check the currency exists")
                    return render(request, "rewards/deleteCampaign.html", {
                        "form":form, 
                        "title":"Delete Campaign"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please check permission access")
                    return render(request, "rewards/deleteCampaign.html", {
                            "form":form, 
                            "title":"Delete Campaign"
                            })
                if response.status_code == 204:
                    messages.info(request, "The  was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 201:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 202:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 200:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/deleteCampaign.html", {
                    "form" : form
                })
        return render(request, "rewards/deleteCampaign.html", {
                "form": form,
                "title": "Delete Campaign"
            })

class AddCampaign(View):
    def get(self, request, *args, **kwargs):
        form = AddCampaignForm()
        return render(request, 'rewards/addCampaign.html', {
            "form": form,
            "title": "UB Loyalty | Campaigns"
        })

    def post(self, request, *args, **kwargs):
        form = AddCampaignForm(request.POST)
        if form.is_valid():
            print("valid")
            #id = form.cleaned_data.get('id')

            post_data = {
                "name": form.cleaned_data.get('name'),
                "starts_at" : form.cleaned_data.get('starts_at'),
                "ends_at" : form.cleaned_data.get('ends_at'),
                "points_expire" : form.cleaned_data.get('points_expiry'),
                "business" : form.cleaned_data.get('business'),
                "currency": form.cleaned_data.get("currency")
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.post(CAMPAIGN_URL, headers = headers, data = post_data)
                print(response)
                res = json.loads(response.text)
                print(res)
                
                if response.status_code == 404:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/addCampaign.html", {
                        "form": form,
                        "title": "Add Campaign"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/addCampaign.html", {
                        "form":form, 
                        "title":"Add Campaign"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please check permission access")
                    return render(request, "rewards/addCampaign.html", {
                            "form":form, 
                            "title":"Add Campaign"
                            })
                if response.status_code == 204:
                    messages.info(request, "The  was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 201:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 202:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 200:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "rewards/addCampaign.html", {
                    "form" : form
                })
        return render(request, "rewards/addCampaign.html", {
                "form": form,
                "title": "Add Campaign"
            })

class EditCampaign(View):
    def get(self, request, *args, **kwargs):
        form = EditCampaignForm()
        return render(request, 'rewards/editCampaign.html', {
            "form": form,
            "title": "UB Loyalty | Campaigns"
        })

    def post(self, request, *args, **kwargs):
        form = EditCampaignForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('choose_campaign')

            post_data = {
                "name": form.cleaned_data.get('name'),
                "starts_at" : form.cleaned_data.get('starts_at'),
                "ends_at" : form.cleaned_data.get('ends_at'),
                "points_expire" : form.cleaned_data.get('points_expiry'),
                "business" : form.cleaned_data.get('business'),
                "currency": form.cleaned_data.get("currency")
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CAMPAIGN_URL + str(id) + '/'
            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                print(response)
                res = json.loads(response.text)
                print(res)
                
                if response.status_code == 404:
                    messages.error(request, "Please check the currency exists")
                    return render(request, "rewards/editCampaign.html", {
                        "form": form,
                        "title": "Edit Campaign"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please check the currency exists")
                    return render(request, "rewards/editCampaign.html", {
                        "form":form, 
                        "title":"Edit Campaign"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please check permission access")
                    return render(request, "rewards/editCampaign.html", {
                            "form":form, 
                            "title":"Edit Campaign"
                            })
                if response.status_code == 204:
                    messages.info(request, "The  was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 201:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 202:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 200:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/editCampaign.html", {
                    "form" : form
                })
        return render(request, "rewards/editCampaign.html", {
                "form": form,
                "title": "Edit Campaign"
            })






































class AccRulesView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"

        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(ACC_RULES, headers = headers)
            res = json.loads(user_response.text)
            accRules = []
            #print(res)
            for idx, _ in enumerate(res):
                d = {
                    'id' : res[idx].get('id'),
                    'value': res[idx].get('value'),
                    'campaign': res[idx].get('campaign'),
                    'category' : res[idx].get('category'),
                    'item': res[idx].get('item'),
                }
                accRules.append(d)
            
            table = AccRulesTable(accRules)
            return render(request, 'rewards/accRules.html', {
            "title": "UB Loyalty | Currency",
            "table" : table 
        })

class DeleteAccRules(View):
    def get(self, request, *args, **kwargs):
        form = DeleteAccRulesForm()
        return render(request, 'rewards/deleteAccRules.html', {
            "form": form,
            "title": "UB Loyalty | Accumulation Rules"
        })

    def post(self, request, *args, **kwargs):
        form = DeleteAccRulesForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('id')

            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = ACC_RULES + str(id) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response.status_code)
                # res = json.loads(response.text)
                # print(res)
                
                if response.status_code == 404:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteAccRules.html", {
                        "form": form,
                        "title": "Delete Accumulation Rules"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteAccRules.html", {
                        "form":form, 
                        "title":"Delete Accumulation Rules"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteAccRules.html", {
                            "form":form, 
                            "title":"Delete Accumulation Rules"
                            })
                if response.status_code == 204:
                    messages.info(request, "The rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 201:
                    messages.info(request, "Your rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 202:
                    messages.info(request, "Your rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 200:
                    messages.info(request, "Your rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/accRules")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/deleteAccRules.html", {
                    "form" : form
                })
        return render(request, "rewards/deleteAccRules.html", {
                "form": form,
                "title": "Delete Accumulation Rules"
            })

class AddAccRules(View):
    def get(self, request, *args, **kwargs):
        form = AddAccRulesForm()
        return render(request, 'rewards/addAccRules.html', {
            "form": form,
            "title": "UB Loyalty | Accumulation Rules"
        })

    def post(self, request, *args, **kwargs):
        form = AddAccRulesForm(request.POST)
        if form.is_valid():
            print("valid")
            #id = form.cleaned_data.get('id')

            post_data = {
                "value": form.cleaned_data.get('value'),
                "campaign" : form.cleaned_data.get('campaign'),
                "category" : form.cleaned_data.get('category'),
                "item" : form.cleaned_data.get('item'),
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.post(ACC_RULES, headers = headers, data = post_data)
                print(response)
                res = json.loads(response.text)
                print(res)
                
                if response.status_code == 404:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/addAccRules.html", {
                        "form": form,
                        "title": "Add Accumulation Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/addAccRules.html", {
                        "form":form, 
                        "title":"Add Accumulation Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/addAccRules.html", {
                            "form":form, 
                            "title":"Add Accumulation Rules"
                            })
                if response.status_code == 204:
                    messages.info(request, "The  was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 201:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 202:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 200:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/addAccRules.html", {
                    "form" : form
                })
        return render(request, "rewards/addAccRules.html", {
                "form": form,
                "title": "Add Accumulation Rules"
            })

class EditAccRules(View):
    def get(self, request, *args, **kwargs):
        form = EditAccRulesForm()
        return render(request, 'rewards/editAccRules.html', {
            "form": form,
            "title": "UB Loyalty | Accumulation Rules"
        })

    def post(self, request, *args, **kwargs):
        form = EditAccRulesForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('id')

            post_data = {
                "value": form.cleaned_data.get('value'),
                "campaign" : form.cleaned_data.get('campaign'),
                "category" : form.cleaned_data.get('category'),
                "item" : form.cleaned_data.get('item'),
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = ACC_RULES + str(id) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                print(response)
                res = json.loads(response.text)
                print(res)
                
                if response.status_code == 404:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/editAccRules.html", {
                        "form": form,
                        "title": "Edit Accumulation Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/editAccRules.html", {
                        "form":form, 
                        "title":"Edit Accumulation Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/editAccRules.html", {
                            "form":form, 
                            "title":"Edit Accumulation Rules"
                            })
                if response.status_code == 204:
                    messages.info(request, "The  was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 201:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 202:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 200:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/editAccRules.html", {
                    "form" : form
                })
        return render(request, "rewards/editAccRules.html", {
                "form": form,
                "title": "Edit Accumulation Rules"
            })



























































































class RedRulesView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"

        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(RED_RULES, headers = headers)
            res = json.loads(user_response.text)
            redRules = []
            
            for idx, _ in enumerate(res):
                d = {
                    'id' : res[idx].get('id'),
                    'reward': res[idx].get('reward'),
                    'image': res[idx].get('image'),
                    'value' : res[idx].get('value'),
                    'campaign': res[idx].get('campaign'),
                }
                redRules.append(d)
            
            table = RedRulesTable(redRules)
            return render(request, 'rewards/redRules.html', {
            "title": "UB Loyalty | Currency",
            "table" : table 
        })

class DeleteRedRules(View):
    def get(self, request, *args, **kwargs):
        form = DeleteRedRulesForm()
        return render(request, 'rewards/deleteRedRules.html', {
            "form": form,
            "title": "UB Loyalty | Redemption Rules"
        })

    def post(self, request, *args, **kwargs):
        form = DeleteAccRulesForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('id')

            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = RED_RULES + str(id) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response.status_code)
                # res = json.loads(response.text)
                # print(res)
                
                if response.status_code == 404:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteAccRules.html", {
                        "form": form,
                        "title": "Delete Accumulation Rules"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteAccRules.html", {
                        "form":form, 
                        "title":"Delete Accumulation Rules"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteAccRules.html", {
                            "form":form, 
                            "title":"Delete Accumulation Rules"
                            })
                if response.status_code == 204:
                    messages.info(request, "The rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 201:
                    messages.info(request, "Your rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 202:
                    messages.info(request, "Your rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 200:
                    messages.info(request, "Your rule was successfully deleted")
                    return HttpResponseRedirect("/rewards/redRules")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/deleteRedRules.html", {
                    "form" : form
                })
        return render(request, "rewards/deleteAccRules.html", {
                "form": form,
                "title": "Delete Accumulation Rules"
            })

class AddRedRules(View):
    def get(self, request, *args, **kwargs):
        form = AddRedRulesForm()
        return render(request, 'rewards/addRedRules.html', {
            "form": form,
            "title": "UB Loyalty | Accumulation Rules"
        })

    def post(self, request, *args, **kwargs):
        form = AddRedRulesForm(request.POST)
        if form.is_valid():
            print("valid")
            #id = form.cleaned_data.get('id')

            post_data = {
                "reward": form.cleaned_data.get('reward'),
                "value": form.cleaned_data.get("value"),
                "campaign" : form.cleaned_data.get('campaign'),
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.post(RED_RULES, headers = headers, data = post_data)
                print(response)
                res = json.loads(response.text)
                print(res)
                
                if response.status_code == 404:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/addRedRules.html", {
                        "form": form,
                        "title": "Add Redemption Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/addRedRules.html", {
                        "form":form, 
                        "title":"Add Redemption Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/addRedRules.html", {
                            "form":form, 
                            "title":"Add Redemption Rules"
                            })
                if response.status_code == 204:
                    messages.info(request, "The rule was successfully added")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 201:
                    messages.info(request, "Your rule was successfully added")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 202:
                    messages.info(request, "Your rule was successfully added")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 200:
                    messages.info(request, "Your rule was successfully added")
                    return HttpResponseRedirect("/rewards/redRules")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/addRedRules.html", {
                    "form" : form
                })
        return render(request, "rewards/addRedRules.html", {
                "form": form,
                "title": "Add Redemption Rules"
            })

class EditRedRules(View):
    def get(self, request, *args, **kwargs):
        form = EditRedRulesForm()
        return render(request, 'rewards/editRedRules.html', {
            "form": form,
            "title": "UB Loyalty | Accumulation Rules"
        })

    def post(self, request, *args, **kwargs):
        form = EditRedRulesForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('id')

            post_data = {
                "reward": form.cleaned_data.get('reward'),
                "value": form.cleaned_data.get("value"),
                "campaign" : form.cleaned_data.get('campaign'),
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            
            EDIT_URL = RED_RULES + str(id) + '/'
            print(EDIT_URL)
            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                print(response)
                res = json.loads(response.text)
                print(response.status_code)
                
                if response.status_code == 404:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/editRedRules.html", {
                        "form": form,
                        "title": "Edit Redemption Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/editRedRules.html", {
                        "form":form, 
                        "title":"Edit Redemption Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, res[key][0])
                    return render(request, "rewards/editRedRules.html", {
                            "form":form, 
                            "title":"Edit Redemption Rules"
                            })
                if response.status_code == 204:
                    messages.info(request, "The rule was successfully edited")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 201:
                    messages.info(request, "Your rule was successfully edited")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 202:
                    messages.info(request, "Your rule was successfully edited")
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 200:
                    messages.info(request, "Your rule was successfully edited")
                    return HttpResponseRedirect("/rewards/redRules")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "rewards/editRedRules.html", {
                    "form" : form
                })
        return render(request, "rewards/editRedRules.html", {
                "form": form,
                "title": "Edit Redemption Rules"
            })












class CurrencyView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"

        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(CURRENCY_URL, headers = headers)
            res = json.loads(user_response.text)
            categories = []

            for idx, _ in enumerate(res):
                temp = res[idx].get('business')
                with open('data.json', 'r') as f:
                    data = json.loads(f.read())
            
                biz = data.get('user').get('employee_of')[0].get('id')
                if temp == biz:
                    d = {
                    'label': res[idx].get('label'),
                    'business' : data.get('user').get('employee_of')[0].get('name')
                    }
                    categories.append(d)

            table = CurrencyTable(categories)
            return render(request, 'rewards/currency.html', {
            "title": "UB Loyalty | Currency",
            "table" : table 
        })

    def post(self, request, *args, **kwargs):
        pass

class DeleteCurrency(View):
    def get(self, request, *args, **kwargs):
        form = DeleteCurrencyForm()
        return render(request, "rewards/deleteCurrency.html", {
            "form": form,
            "title": "Add Currency"
        })  

    def post(self, request, *args, **kwargs):
        form = DeleteCurrencyForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('currency')
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CURRENCY_URL + str(id) + '/'
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response.status_code)

                
                if response.status_code == 404:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/deleteCurrency.html", {
                        "form": form,
                        "title": "Delete Currency"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/deleteCurrency.html", {
                        "form":form, 
                        "title":"Delete Currency"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please check permission access")
                    return render(request, "rewards/deleteCurrency.html", {
                            "form":form, 
                            "title":"Delete Currency"
                            })
                if response.status_code == 204:
                    
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 201:
                    
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 202:
                    
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 200:
                    
                    return HttpResponseRedirect("/rewards/currency")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "rewards/deleteCurrency.html", {
                    "form" : form
                })
        return render(request, "rewards/deleteCurrency.html", {
                "form": form,
                "title": "Delete Currency"
            })

class AddCurrency(View):
    def get(self, request, *args, **kwargs):
        form = AddCurrencyForm()
        return render(request, "rewards/addCurrency.html", {
            "form": form,
            "title": "Add Currency"
        })  

    def post(self, request, *args, **kwargs):
        form = AddCurrencyForm(request.POST)
        if form.is_valid():
            print("valid")

            post_data = {
                "label": form.cleaned_data.get('label'),
                "business": form.cleaned_data.get("business")
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.post(CURRENCY_URL, headers = headers, data = post_data)
                print(response)

                with open('currency.json') as f:
                    try:
                        data = json.load(f)
                        print("Done")
                    except ValueError:
                        data = {}
                        data['currency'] = []
                
                new = eval(response.text)
                data['currency'].append(new)
                with open('currency.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(data, indent=4))

                res = json.loads(response.text)
                
                if response.status_code == 404:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/addCurrency.html", {
                        "form": form,
                        "title": "Add Currency"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/addCurrency.html", {
                        "form":form, 
                        "title":"Add Currency"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please check permission access")
                    return render(request, "rewards/addCurrency.html", {
                            "form":form, 
                            "title":"Add Currency"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 201:
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 202:
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 200:
                    return HttpResponseRedirect("/rewards/currency")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "rewards/addCurrency.html", {
                    "form" : form
                })
        return render(request, "rewards/addCurrency.html", {
                "form": form,
                "title": "Add Currency"
            })

class EditCurrency(View):
    def get(self, request, *args, **kwargs):
        form = EditCurrencyForm()
        return render(request, "rewards/editCurrency.html", {
            "form": form,
            "title": "Add Currency"
        })  

    def post(self, request, *args, **kwargs):
        form = EditCurrencyForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('currency')

            post_data = {
                "label": form.cleaned_data.get('new_label'),
                "business": form.cleaned_data.get("business")
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CURRENCY_URL + str(id) + '/'
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                #print(response)
                res = json.loads(response.text)
                #print(res)
                
                currency_response = requests.get(CURRENCY_URL, headers = headers)
                curr_res = json.loads(currency_response.text)
                #print(curr_res)

                # with open('currency.json') as f:
                #     data = {}
                #     data['currency'] = []
                #     for item in curr_res:
                #         if item['business'] == res['business']:
                #             data['currency'].append(item)
                
                # with open('currency.json', 'w', encoding='utf-8') as f:
                #             f.write(json.dump(data, f, indent=4))
                
                if response.status_code == 404:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/editCurrency.html", {
                        "form": form,
                        "title": "Edit Currency"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/editCurrency.html", {
                        "form":form, 
                        "title":"Edit Currency"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please check permission access")
                    return render(request, "rewards/editCurrency.html", {
                            "form":form, 
                            "title":"Edit Currency"
                            })
                if response.status_code == 204:
                    
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 201:
                    
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 202:
                    
                    return HttpResponseRedirect("/rewards/currency")
                if response.status_code == 200:
                    
                    return HttpResponseRedirect("/rewards/currency")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "rewards/editCurrency.html", {
                    "form" : form
                })
        return render(request, "rewards/editCurrency.html", {
                "form": form,
                "title": "Edit Currency"
            })
