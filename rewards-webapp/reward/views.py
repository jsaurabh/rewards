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
            user_data = json.loads(f.read())
        
        token = user_data.get('token')
        tokenh = f"Token {token}"
        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(CAMPAIGN_URL, headers = headers)
            res = json.loads(user_response.text)
            campaigns = []
            campaigns.append(res)

            #print(res)
            with open('campaigns.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(campaigns, indent=4))

            try:
                with open('currency.json', 'r') as f:
                    curr = json.loads(f.read())
            except:
                curr = ""
            
            try:
                with open("campaigns.json", 'r') as f:
                    data = json.loads(f.read())
            except:
                data = ""

            employee_struct = {}
            for item in user_data.get('user').get('employee_of'):
                employee_struct[item.get('id')] = item.get('name')
            
            currency_struct = {}
            for item in curr['currency']:
                currency_struct[item.get('id')] = item.get('label')

            print(currency_struct)
            camp = []
            campaign = []
            for item in data[0]:
                if item.get('business') in employee_struct:
                    campaign.append(item)
                    d = {
                        'id' : item.get('id'),
                        'name': item.get('name'),
                        'start': item.get('starts_at'),
                        'end' : item.get('ends_at'),
                        'expiry': item.get('points_expire_after'),
                        'business': employee_struct[item.get('business')],
                        'currency': currency_struct[item.get('currency')]
                        }
                    camp.append(d)

            with open('campaigns.json', 'w', encoding = 'utf-8') as f:
                json.dump(campaign, f, indent= 4)
            table = CampaignTable(camp)
            return render(request, 'rewards/rewards.html', {
            "title": "UB Loyalty | Currency",
            "table" : table 
        })

    def post(self, *args, **kwargs):
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
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/editCampaign.html", {
                        "form": form,
                        "title": "Edit Campaign"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please check the currency exists")
                    return render(request, "rewards/editCampaign.html", {
                        "form":form, 
                        "title":"Edit Campaign"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please check permission access")
                    return render(request, "rewards/editCampaign.html", {
                            "form":form, 
                            "title":"Edit Campaign"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 201:
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 202:
                    return HttpResponseRedirect("/rewards/")
                if response.status_code == 200:
                    return HttpResponseRedirect("/rewards/")    
            else:
                form.add_error(None, "Your request could not be completed")
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
        
        with open('campaigns.json', 'r') as f:
            campaign = json.loads(f.read())

        if len(campaign) == 0:
            return HttpResponseRedirect("/rewards")

        with open('catalog.json', 'r') as f:
            category = json.loads(f.read())

        token = data.get('token')

        campaign_ids = set()
        campaign_d = {}
        category_d = {}
        items = {} 

        for ctgry in category:
            ids = ctgry.get('id')
            for item in ctgry.get('items'):
                items[item['id']] = item['name']
            category_d[ids] = ctgry.get('name')

        for cmpgn in campaign:
            ids = cmpgn.get('id')
            campaign_ids.add(ids)
            campaign_d[ids] = cmpgn.get('name')
            
        tokenh = f"Token {token}"
        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(ACC_RULES, headers = headers)
            res = json.loads(user_response.text)

            accRules = []
            for idx, _ in enumerate(res):
                id = res[idx].get('campaign')
                
                if id in campaign_ids:
                    
                    if res[idx].get('category') is not None:
                         cat = category_d[res[idx].get('category')]
                    else:
                        cat = None

                    if res[idx].get('item') is not None:
                        it = items[res[idx].get('item')]
                    else:
                        it = None
                    
                    d = {
                    'id': res[idx].get('id'),
                    'value': res[idx].get('value'),
                    'campaign': campaign_d[res[idx].get('campaign')],
                    'category' : cat,
                    'item': it}
                    accRules.append(d)
                else:
                    pass
            print(accRules)
            with open('rules.json', 'w', encoding = 'utf-8') as f:
                json.dump(accRules, f, indent= 4)
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
            id = form.cleaned_data.get('rule_choice')

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
                
                if response.status_code == 404:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteRedRules.html", {
                        "form": form,
                        "title": "Delete Accumulation Rules"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteRedRules.html", {
                        "form":form, 
                        "title":"Delete Accumulation Rules"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please validate your input")
                    return render(request, "rewards/deleteRedRules.html", {
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
        return render(request, "rewards/deleteRedRules.html", {
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
            choice = form.cleaned_data.get("rule")
            if choice == 'C':
                post_data = {
                "value": form.cleaned_data.get('value'),
                "campaign" : form.cleaned_data.get('campaign'),
                "category" : form.cleaned_data.get('category'),
                "item" : "",
            }
            else:
                post_data = {
                "value": form.cleaned_data.get('value'),
                "campaign" : form.cleaned_data.get('campaign'),
                "category" : "",
                "item": form.cleaned_data.get("item"),
                }

            print(post_data)

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
                        form.add_error(key, res[key][0])
                    return render(request, "rewards/addAccRules.html", {
                        "form": form,
                        "title": "Add Accumulation Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        form.add_error(key, res[key][0])
                    return render(request, "rewards/addAccRules.html", {
                        "form":form, 
                        "title":"Add Accumulation Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(key, res[key][0])
                    return render(request, "rewards/addAccRules.html", {
                            "form":form, 
                            "title":"Add Accumulation Rules"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 201:
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 202:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 200:
                    messages.info(request, "Your campaign was successfully added")
                    return HttpResponseRedirect("/rewards/accRules")    
            else:
                form.add_error(None, "Your request could not be completed")
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
            id = form.cleaned_data.get('rule_choice')

            choice = form.cleaned_data.get("rule")
            if choice == 'C':
                post_data = {
                "value": form.cleaned_data.get('value'),
                "campaign" : form.cleaned_data.get('campaign'),
                "category" : form.cleaned_data.get('category'),
                "item" : "",
            }
            else:
                post_data = {
                "value": form.cleaned_data.get('value'),
                "campaign" : form.cleaned_data.get('campaign'),
                "category" : "",
                "item": form.cleaned_data.get("item"),
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
                        form.add_error(None, res[key][0])
                    return render(request, "rewards/editAccRules.html", {
                        "form": form,
                        "title": "Edit Accumulation Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key][0])
                    return render(request, "rewards/editAccRules.html", {
                        "form":form, 
                        "title":"Edit Accumulation Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, res[key][0])
                    return render(request, "rewards/editAccRules.html", {
                            "form":form, 
                            "title":"Edit Accumulation Rules"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 201:
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 202:
                    return HttpResponseRedirect("/rewards/accRules")
                if response.status_code == 200:
                    return HttpResponseRedirect("/rewards/accRules")    
            else:
                form.add_error(key, "Your request could not be completed")
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

        with open('campaigns.json', 'r') as f:
            campaign = json.loads(f.read())

        if len(campaign) == 0:
            return HttpResponseRedirect("/rewards")
        token = data.get('token')
        
        campaign_ids = set()
        campaign_d = {}

        for cmpgn in campaign:
            ids = cmpgn.get('id')
            campaign_ids.add(ids)
            campaign_d[ids] = cmpgn.get('name')
            
        token = data.get('token')
        tokenh = f"Token {token}"
        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(RED_RULES, headers = headers)
            res = json.loads(user_response.text)
            redRules = []
            for idx, _ in enumerate(res):
                id = res[idx].get('campaign')
                
                if id in campaign_ids:
                    d = {
                    'id': res[idx].get('id'),
                    'value': res[idx].get('value'),
                    'campaign': campaign_d[res[idx].get('campaign')],
                    'reward' : res[idx].get('reward'),
                    }
                    redRules.append(d)
            
            print(redRules)

            with open('redRules.json', 'w', encoding = 'utf-8') as f:
                json.dump(redRules, f, indent= 4)
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
            id = form.cleaned_data.get('reward_choice')

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
                
                if response.status_code == 404:
                    form.add_error(None, "Please validate your input")
                    return render(request, "rewards/deleteRedRules.html", {
                        "form": form,
                        "title": "Delete Redemption Rules"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please validate your input")
                    return render(request, "rewards/deleteRedRules.html", {
                        "form":form, 
                        "title":"Delete Redemption Rules"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please validate your input")
                    return render(request, "rewards/deleteRedRules.html", {
                            "form":form, 
                            "title":"Delete Redemption Rules"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 201:
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 202:
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 200:
                    return HttpResponseRedirect("/rewards/redRules")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "rewards/deleteRedRules.html", {
                    "form" : form
                })
        return render(request, "rewards/deleteRedRules.html", {
                "form": form,
                "title": "Delete Redemption Rules"
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
            id = form.cleaned_data.get('reward_choice')

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
                        form.add_error(None, res[key][0])
                    return render(request, "rewards/editRedRules.html", {
                        "form": form,
                        "title": "Edit Redemption Rules"
                    })
                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key][0])
                    return render(request, "rewards/editRedRules.html", {
                        "form":form, 
                        "title":"Edit Redemption Rules"
                        })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, res[key][0])
                    return render(request, "rewards/editRedRules.html", {
                            "form":form, 
                            "title":"Edit Redemption Rules"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 201:
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 202:
                    return HttpResponseRedirect("/rewards/redRules")
                if response.status_code == 200:
                    return HttpResponseRedirect("/rewards/redRules")    
            else:
                form.add_error(None, "Your request could not be completed")
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
            currencies = {}
            currencies['currency'] = []
            currencies["currency"].append(res)
            with open('currency.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(currencies, indent=4))
            
            with open('currency.json', 'r') as f:
                data = json.loads(f.read())
            with open('data.json', 'r') as f:
                user_data = json.loads(f.read())
            
            employee_struct = {}
            for item in user_data.get('user').get('employee_of'):
                #employee_struct.add(item.get('id'))
                employee_struct[item.get('id')] = item.get('name')
            
            currency = {}
            currency['currency'] = []
            for item in data['currency'][0]:
                if item.get('business') in employee_struct:
                    currency['currency'].append(item)
                    d = {
                        'label': item.get('label'),
                        'business' : employee_struct[item.get('business')]
                    }
                    categories.append(d)
            
            with open('currency.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(currency, indent=4))
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
