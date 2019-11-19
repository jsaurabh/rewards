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
        #id = data.get('user').get('id')
        READ_URL = CATEGORY_READ_URL + str(16) + '/'
        headers = {"Authorization": tokenh}

        if token:
            user_response = requests.get(READ_URL, headers = headers)
            res = json.loads(user_response.text)
            categories = []
            for idx, _ in enumerate(res):
                d = {
                    'Category_ID' : res[idx].get('id'),
                    'name': res[idx].get('name'),
                    # 'items': res[idx].get('items')
                }
                categories.append(d)

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
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            print("valid")
        
            post_data = {
                "name": form.cleaned_data.get('name'), 
                #### CHANGE TO CURRENT BUSINESS
                "business": 16
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CATEGORY_UPDATE_URL 
            print(EDIT_URL)

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                #print(post_data)
                response = requests.post(EDIT_URL, headers = headers, data = post_data)
                res = json.loads(response.text)
                print(response)
                print(res)

                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key])
                        return render(request, "catalog/addCatalog.html", {
                            "form":form, 
                            "title":"Add Category"
                            })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, "Please check permission access")
                        return render(request, "catalog/addCatalog.html", {
                            "form":form, 
                            "title":"Add Category"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your category was successfully added")
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 202:
                    messages.info(request, "Your category was successfully added")
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 200:
                    messages.info(request, "Your category was successfully added")
                    return HttpResponseRedirect("/catalog/")    
            else:
                messages.error(request, "Your request could not be completed")
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
        form = EditCategoryForm(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('id')
            post_data = {
                "name": form.cleaned_data.get('name'), 
                #### CHANGE TO CURRENT BUSINESS
                "business": 16
            }
            
            with open('data.json', 'r') as f:
                data = json.loads(f.read())
            
            token = data.get('token')
            EDIT_URL = CATEGORY_UPDATE_URL + str(id) + '/'
            print(EDIT_URL)
            #USER_URL = USER_READ_URL + str(data.get('user').get('id')) + '/'

            if token:
                print("Got token")
                tokenh = f"Token {token}"
                headers = {"Authorization": tokenh}
                print(post_data)
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                res = json.loads(response.text)
                print(response)
                print(res)
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key][0].capitalize())
                        return render(request, "catalog/editCatalog.html", {
                            "form":form, 
                            "title":"Edit Business"
                            })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, "Please check permission access")
                        return render(request, "catalog/editCatalog.html", {
                            "form":form, 
                            "title":"Edit Catalogs"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your catalog was successfully edited")

                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 202:
                    messages.info(request, "Your catalog was successfully edited")

                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 200:
                    messages.info(request, "Your catalog was successfully edited")

                    return HttpResponseRedirect("/catalog/")    
            else:
                messages.error(request, "Your request could not be completed")
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
            id = form.cleaned_data.get('id')
            
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
                # res = json.loads(response.text)
                # print(response)
                # print(res)
                
                if response.status_code == 404:
                    messages.error(request, "Please check the category exists")
                    return render(request, "catalog/deleteCatalog.html", {
                        "form": form,
                        "title": "Delete Category"
                    })
                if response.status_code == 400:
                    messages.error(request, "Please check the category exists")
                    return render(request, "catalog/deleteCatalog.html", {
                        "form":form, 
                        "title":"Delete Category"
                        })
                if response.status_code == 405:
                    messages.error(request, "Please check permission access")
                    return render(request, "catalog/deleteCatalog.html", {
                            "form":form, 
                            "title":"Delete Category"
                            })
                if response.status_code == 204:
                    messages.info(request, "The category was successfully deleted")
                    return HttpResponseRedirect("/catalog")
                if response.status_code == 201:
                    messages.info(request, "Your category was successfully deleted")
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 202:
                    messages.info(request, "Your category was successfully deleted")
                    return HttpResponseRedirect("/catalog/")
                if response.status_code == 200:
                    messages.info(request, "Your category was successfully deleted")
                    return HttpResponseRedirect("/catalog/")    
            else:
                messages.error(request, "Your request could not be completed")
                return render(request, "catalog/deleteCatalog.html", {
                    "form" : form
                })
        return render(request, "catalog/deleteCatalog.html", {
                "form": form,
                "title": "Delete Category"
            })

class AddItemsView(View):
    def get(self, request, *args, **kwargs):
        form = AddItems()
        return render(request, "catalog/add-items.html", {
            "form": form,
            "title": "Add Items"
        })    

    def post(self, request, *args, **kwargs):
        form = AddItems(request.POST)
        if form.is_valid():
            print("valid")
        
            post_data = {
                "name": form.cleaned_data.get('name'),
                "image": None,
                #"image": form.cleaned_data.get('image'),
                #### CHANGE TO CURRENT BUSINESS
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
                response = requests.post(EDIT_URL, headers = headers, data = post_data)
                res = json.loads(response.text)
                print(response)
                print(res)
                
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key])
                        return render(request, "catalog/add-items.html", {
                            "form":form, 
                            "title":"Add Items"
                            })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, "Please check permission access")
                        return render(request, "catalog/add-items.html", {
                            "form":form, 
                            "title":"Add Items"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your item was successfully added")
                    return HttpResponseRedirect("/catalog/items/")
                if response.status_code == 202:
                    messages.info(request, "Your item was successfully added")
                    return HttpResponseRedirect("/catalog/items/")
                if response.status_code == 200:
                    messages.info(request, "Your item was successfully added")
                    return HttpResponseRedirect("/catalog/items/")    
            else:
                messages.error(request, "Your request could not be completed")
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
        form = EditItems(request.POST)
        if form.is_valid():
            print("valid")
            id = form.cleaned_data.get('id')
            post_data = {
                "name": form.cleaned_data.get('name'),
                "image": None,
                #"image": form.cleaned_data.get('image'),
                #### CHANGE TO CURRENT BUSINESS
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
                response = requests.put(EDIT_URL, headers = headers, data = post_data)
                res = json.loads(response.text)
                print(response)
                print(res)
                
                if response.status_code == 400:
                    for key in res:
                        messages.error(request, res[key])
                        return render(request, "catalog/edit-items.html", {
                            "form":form, 
                            "title":"Edit Items"
                            })
                if response.status_code == 405:
                    for key in res:
                        messages.error(request, "Please check permission access")
                        return render(request, "catalog/edit-items.html", {
                            "form":form, 
                            "title":"Edit Items"
                            })
                if response.status_code == 201:
                    messages.info(request, "Your item was successfully edited")
                    return HttpResponseRedirect("/catalog/items/")
                if response.status_code == 202:
                    messages.info(request, "Your item was successfully edited")
                    return HttpResponseRedirect("/catalog/items/")
                if response.status_code == 200:
                    messages.info(request, "Your item was successfully edited")
                    return HttpResponseRedirect("/catalog/items/")    
            else:
                messages.error(request, "Your request could not be completed")
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
            id = form.cleaned_data.get('id')
            
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
        #categories = []
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
            return render(request, 'catalog/items-v.html', {
             "title": "UB Loyalty | Items",
             "form" : form, 
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