import json

# def users(response):
#     res = json.loads(response.text)
#     token = res.get('token')
#     user = res.get('user')
#     customer = res.get('customer_of')
#     employee = res.get('employee_of')

class User:
    def __init__(self, data):
        self.data = data
        self.token = ""
        self.user = {}
        self.customerOf = {}
        self.employeeOf = {}

    def __repr__(self):
        return self.user
    
    def setToken(self):
        self.token = self.data.get('token')

    def setUser(self):
        self.user = self.data.get('user')
    
    def setCustomer(self):
        self.customerOf = self.user.get('customer_of')

    def setEmployees(self):
        self.employeeOf = self.user.get('employee_of')

    def getToken(self):
        return self.token
    
    def getUser(self):
        return self.user

    def getEmployees(self):
        return self.employeeOf

    def getCustomer(self):
        return self.customerOf
    
    def getObject(self):
        return self.token, self.user, self.employeeOf, self.customerOf
