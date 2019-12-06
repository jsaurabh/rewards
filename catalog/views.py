from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import AddCategoryForm, DeleteCategoryForm, EditCategoryForm
from .forms import AddItems, EditItems, DeleteItems
from .forms import ItemViewForm
from django.http import HttpResponseRedirect
import requests, json
from django.views.generic import View
from dashboard.users import User
from .tables import CategoryTable, ItemTable

# API routes 
CATEGORY_READ_URL = "https://webdev.cse.buffalo.edu/rewards/catalog/business/"
CATEGORY_UPDATE_URL = "https://webdev.cse.buffalo.edu/rewards/catalog/categories/"
ITEMS_UPDATE_URL = "https://webdev.cse.buffalo.edu/rewards/catalog/items/"

# Create your views here.
class CatalogView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"
        try:
            id = data.get('user').get('employee_of')[0].get('id')
        except:
            return render(request, 'catalog/items-v.html', {
                'form': ItemViewForm([]),
                "table": ItemTable("")
            })
        
        READ_URL = CATEGORY_READ_URL + str(id) + '/'
        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(READ_URL, headers = headers)
            res = json.loads(user_response.text)
            print(res)
            
            with open('catalog.json', 'w', encoding='utf-8') as f:
                json.dump(res, f, indent=4)
            
            categories = []
            # if res:
            #     table = CategoryTable(categories)
            #else:
            for idx, _ in enumerate(res):
                    d = {
                        'name': res[idx].get('name'),
                        # 'items': res[idx].get('items')
                    }
                    categories.append(d)
            #print(categories)
            table = CategoryTable(categories)
            return render(request, 'catalog/catalog.html', {
            "title": "UB Loyalty | Catalog",
            "table" : table 
        })

    def post(self, request, *args, **kwargs):
        pass

class AddCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = AddCategoryForm()
        return render(request, "catalog/addCatalog.html", {
            "form": form,
            "title": "Add Category"
        })    

    def post(self, request, *args, **kwargs):

        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            logo = form.cleaned_data.get('logo')
            post_data = {
                "name": form.cleaned_data.get('name'), 
                "business": form.cleaned_data.get('business')
            }   
            print(post_data)
    
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CATEGORY_UPDATE_URL 
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                
                response = requests.post(EDIT_URL, headers = headers, data = post_data, files = {"logo": logo})
                res = json.loads(response.text)

                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key])
                        return render(request, "catalog/addCatalog.html", {
                            "form":form, 
                            "title":"Add Category"
                            })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, "Please check permission access")
                        return render(request, "catalog/addCatalog.html", {
                            "form":form, 
                            "title":"Add Category"
                            })
                if response.status_code == 201:
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 202:
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 200:
                    return HttpResponseRedirect("/catalog/")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "catalog/addCatalog.html", {
                    "form" : form
                })
        return render(request, "catalog/addCatalog.html", {
                "form": form,
                "title": "Add Category"
            })

class EditCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = EditCategoryForm()
        return render(request, "catalog/editCatalog.html", {
            "form": form,
            "title": "Edit Category"
        })

    def post(self, request, *args, **kwargs):
        
        form = EditCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            id = form.cleaned_data.get('catalog_choice')
            logo = form.cleaned_data.get('logo')

            post_data = {
                "name": form.cleaned_data.get('name'), 
                "business": form.cleaned_data.get('business')
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CATEGORY_UPDATE_URL + str(id) + '/'
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                print(post_data)
                response = requests.put(EDIT_URL, headers = headers, data = post_data, files = {"logo": logo})
                res = json.loads(response.text)
                #print(response)
                #print(res)
                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key][0].capitalize())
                        return render(request, "catalog/editCatalog.html", {
                            "form":form, 
                            "title":"Edit Business"
                            })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, "Please check permission access")
                        return render(request, "catalog/editCatalog.html", {
                            "form":form, 
                            "title":"Edit Catalogs"
                            })
                if response.status_code == 201:
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 202:
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 200:
                    return HttpResponseRedirect("/catalog/")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "catalog/editCatalog.html", {
                    "form" : form
                })
        return render(request, "catalog/editCatalog.html", {
                "form": form,
                "title": "Edit Business"
            })

class DeleteCategoryView(View):
    def get(self, request, *args, **kwargs):
        form = DeleteCategoryForm()
        return render(request, "catalog/deleteCatalog.html", {
            "form": form,
            "title": "Delete Category"
        })  

    def post(self, request, *args, **kwargs):

        form = DeleteCategoryForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('catalog_choice')
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CATEGORY_UPDATE_URL + str(id) + '/'
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response.status_code)
                
                if response.status_code == 404:
                    form.add_error(None, "Please check the category exists")
                    return render(request, "catalog/deleteCatalog.html", {
                        "form": form,
                        "title": "Delete Category"
                    })
                if response.status_code == 400:
                    form.add_error(None, "Please check the category exists")
                    return render(request, "catalog/deleteCatalog.html", {
                        "form":form, 
                        "title":"Delete Category"
                        })
                if response.status_code == 405:
                    form.add_error(None, "Please check permission access")
                    return render(request, "catalog/deleteCatalog.html", {
                            "form":form, 
                            "title":"Delete Category"
                            })
                if response.status_code == 204:
                    return HttpResponseRedirect("/catalog")
                if response.status_code == 201:
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 202:
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 200:
                    return HttpResponseRedirect("/catalog/")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "catalog/deleteCatalog.html", {
                    "form" : form
                })
        return render(request, "catalog/deleteCatalog.html", {
                "form": form,
                "title": "Delete Category"
            })


##########################
# ITEMS
##########################


class AddItemsView(View):
    def get(self, request, *args, **kwargs):
        form = AddItems()
        return render(request, "catalog/add-items.html", {
            "form": form,
            "title": "Add Items"
        })    

    def post(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        form = AddItems(request.POST, request.FILES)
        if form.is_valid():
            print("valid")

            image = form.cleaned_data.get('logo')
            post_data = {
                "name": form.cleaned_data.get('name'),
                "image": None,
                "category": form.cleaned_data.get("category")
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = ITEMS_UPDATE_URL 

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                print(post_data)
                response = requests.post(EDIT_URL, headers = headers, data = post_data, files = {"logo": image})
                res = json.loads(response.text)
                print(response)
                print(res)
                
                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key])
                        return render(request, "catalog/add-items.html", {
                            "form":form, 
                            "title":"Add Items"
                            })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, "Please check permission access")
                        return render(request, "catalog/add-items.html", {
                            "form":form, 
                            "title":"Add Items"
                            })
                if response.status_code == 201:
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 202:
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 200:
                    return HttpResponseRedirect("/catalog/items")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "catalog/add-items.html", {
                    "form" : form
                })
        return render(request, "catalog/add-items.html", {
                "form": form,
                "title": "Add Items"
            })

class EditItemsView(View):
    def get(self, request, *args, **kwargs):
        form = EditItems()
        return render(request, "catalog/edit-items.html", {
            "form": form,
            "title": "Edit Items"
        }) 

    def post(self, request, *args, **kwargs):
        
        form = EditItems(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('item_choice')
            image = form.cleaned_data.get('logo')
            
            post_data = {
                "name": form.cleaned_data.get('name'),
                "category": form.cleaned_data.get("category")
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = ITEMS_UPDATE_URL + str(id) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                print(post_data)
                response = requests.put(EDIT_URL, headers = headers, data = post_data, files = {"logo": image})
                res = json.loads(response.text)
                #print(response)
                #print(res)
                
                if response.status_code == 400:
                    for key in res:
                        form.add_error(None, res[key])
                        return render(request, "catalog/edit-items.html", {
                            "form":form, 
                            "title":"Edit Items"
                            })
                if response.status_code == 405:
                    for key in res:
                        form.add_error(None, "Please check permission access")
                        return render(request, "catalog/edit-items.html", {
                            "form":form, 
                            "title":"Edit Items"
                            })
                if response.status_code == 201:
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 202:
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 200:
                    return HttpResponseRedirect("/catalog/items")    
            else:
                form.add_error(None, "Your request could not be completed")
                return render(request, "catalog/edit-items.html", {
                    "form" : form
                })
        return render(request, "catalog/edit-items.html", {
                "form": form,
                "title": "Edit Items"
            })

class DeleteItemsView(View):

    def get(self, request, *args, **kwargs):
        form = DeleteItems()
        return render(request, "catalog/delete-items.html", {
            "form": form,
            "title": "Delete Item"
        }) 

    def post(self, request, *args, **kwargs):
        form = DeleteItems(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('item_choice')
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = ITEMS_UPDATE_URL + str(id) + '/'
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                response = requests.delete(EDIT_URL, headers = headers)
                print(response.status_code)
                # res = json.loads(response.text)
                # print(response)
                # print(res)
                
                if response.status_code == 404:
                    messages.error(request, "Please check the item exists")
                    return render(request, "catalog/delete-items.html", {
                        "form": form,
                        "title": "Delete Item"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please check the item exists")
                    return render(request, "catalog/delete-items.html", {
                        "form":form, 
                        "title":"Delete Item"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please check permission access")
                    return render(request, "catalog/delete-items.html", {
                            "form":form, 
                            "title":"Delete Item"
                            })
                if response.status_code == 204:
                    messages.info(request, "The item was successfully deleted")
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 201:
                    messages.info(request, "Your item was successfully deleted")
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 202:
                    messages.info(request, "Your item was successfully deleted")
                    return HttpResponseRedirect("/catalog/items")
                if response.status_code == 200:
                    messages.info(request, "Your item was successfully deleted")
                    return HttpResponseRedirect("/catalog/items")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "catalog/delete-items.html", {
                    "form" : form
                })
        return render(request, "catalog/delete-items.html", {
                "form": form,
                "title": "Delete Item"
            })

class ItemView(View):
    def __init__(self):
        self.categories = []
    
    def get(self, request, *args, **kwargs):
        
        with open('data.json', 'r') as f:
                data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"
        try:
            id = data.get('user').get('employee_of')[0].get('id')
        except:
            return render(request, 'catalog/items-v.html', {
                'form': ItemViewForm([]),
                "table": ItemTable("")
            })
        USER_URL = CATEGORY_READ_URL + str(id) + '/'
        
        headers = {"Authorization": tokenh}

        if token:
            response = requests.get(USER_URL, headers = headers)
            res = json.loads(response.text)

            user_response = requests.get(USER_URL, headers = headers)
            res = json.loads(user_response.text)
            print(res)
            
            with open('catalog.json', 'w', encoding='utf-8') as f:
                json.dump(res, f, indent=4)
            for idx, val in enumerate(res):
                n = val.get('name') + " ID: " + str(val.get('id'))
                self.categories.append((val.get('id'), n))
            
            form = ItemViewForm(self.categories)
            categories = []

            for idx, _ in enumerate(res):
                items = res[idx].get('items')
                if items:
                    for item in items:
                        d = {'name': item['name'], 'category': res[idx].get('name')}
                        categories.append(d)
    
            table = ItemTable(categories)

            return render(request, 'catalog/items-v.html', {
             "title": "UB Loyalty | Items",
             #"form" : form, 
             "table": table
        })
    
    def post(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
                data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"
        id = 16 ###SELECT BUSINESS HERE
        USER_URL = CATEGORY_READ_URL + str(id) + '/'
        headers = {"Authorization": tokenh}

        if token:
            response = requests.get(USER_URL, headers = headers)
            res = json.loads(response.text)
            #print(res)
            for idx, val in enumerate(res):
                n = val.get('name') + " ID: " + str(val.get('id'))
                self.categories.append((val.get('id'), n))
            form = ItemViewForm(self.categories)
            table = ItemTable(res[0].get('items'))
            return render(request, 'catalog/items.html', {
             "title": "UB Loyalty | Items",
             "form" : form, 
             "table": table
        })