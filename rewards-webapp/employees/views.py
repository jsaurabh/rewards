from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import AddEmployeeForm, DeleteEmployeeForm
from django.http import HttpResponseRedirect
import requests, json
from django.views.generic import View
from dashboard.users import User

# API routes
EMPLOYEE_READ_URL = "https://webdev.cse.buffalo.edu/rewards/programs/businesses/"

# Create your views here.
class EmployeeView(View):
    def get(self, request, *args, **kwargs):
        with open('data.json', 'r') as f:
                data = json.loads(f.read())
        
        token = data.get('token')
        tokenh = f"Token {token}"
        id = data.get('user').get('id')
        EMPLOYEE_URL = EMPLOYEE_READ_URL + str(16) + '/employees'
        headers = {"Authorization": tokenh}

        if token:
            employee_response = requests.get(EMPLOYEE_READ_URL, headers = headers)
            res = json.loads(employee_response.text)
            #data['user'] = res
            businesses = res.get('employee_of')
            table = NameTable(businesses)
            return render(request, 'business.html', {
            "title": "UB Loyalty | Business",
            "table" : table 
        })
        return render(request, 'employees/employees.html', {
        })
    
    def post(self, request, *args, **kwargs):
        pass

class DeleteEmployeeView(View):
    def get(self, request, *args, **kwargs):
        form = AddEmployeeForm()
        return render(request, "employees/employees.html", {
            "form":form,
            "title":"Login"
        })
    
    def post(self, request, *args, **kwargs):
        pass

class AddEmployeeView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass