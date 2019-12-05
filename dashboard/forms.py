from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.utils.safestring import mark_safe
import json

class BusinessCreationForm(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Business Name</strong>"), required = False, max_length=50, min_length=1)
    phone = PhoneNumberField(label = "Phone Number", required = False, region="US")
    url = forms.URLField(label = "URL", help_text = "Enter a web address", max_length = 200, required = False)
    address = forms.CharField(label = "Business Address", required = False)
    #logo = forms.ImageField(help_text = "Upload a logo for your business", required = False)
    #publish = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(BusinessCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': "Business Name",
            'placeholder': "Name for your business"
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'name': "Phone Number"
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'name': "Address"
        })
        self.fields['url'].widget.attrs.update({
            'class': 'form-control',
            'name': "URL"
        })
        # self.fields['publish'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': "URL",
        #     'style': 'width:20px;height:20px'
        # })
        # self.fields['logo'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': "Choose Logo"
        # })

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("name")

        if not name:
            self.add_error("name", "Please enter a name for your business")

        return super(BusinessCreationForm, self).clean(*args, **kwargs)

class BusinessDeleteForm(forms.Form):
    
    business = forms.ChoiceField(choices=[])    

    def __init__(self, *args, **kwargs):
        super(BusinessDeleteForm, self).__init__(*args, **kwargs)
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        self.choices = []
        for biz in data.get('user').get('employee_of'):
            self.choices.append((biz.get('id'), biz.get('name')))
        self.initial['business'] = 'None'
        self.fields['business'] = forms.ChoiceField(initial = None, choices = self.choices)
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name'
        })
    
    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get('business')

        if not name:
            self.add_error(None, "Please select a business to delete")

class BusinessEditForm(forms.Form):

    business = forms.ChoiceField(choices=[])
    name = forms.CharField(label = mark_safe("<strong>*Business Name</strong>"), required = False, 
                           max_length=50, min_length=1, help_text = "Enter a new name for the business")
    phone = PhoneNumberField(label = "Phone Number", required = False, region="US")
    url = forms.URLField(label = "URL", help_text = "Enter a web address", max_length = 200, required = False)
    address = forms.CharField(label = "Business Address", required = False)
    #logo = forms.ImageField(help_text = "Upload a logo for your business", required = False)
    publish = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(BusinessEditForm, self).__init__(*args, **kwargs)
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for biz in data.get('user').get('employee_of'):
            choices.append((biz.get('id'), biz.get('name')))
        self.initial['business'] = 'None'
        self.fields['business'] = forms.ChoiceField(choices=choices)
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business id'
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': "Business Name"
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'name': "Phone Number"
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'name': "Address"
        })
        self.fields['url'].widget.attrs.update({
            'class': 'form-control',
            'name': "URL"
        })
        # self.fields['logo'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': "Choose Logo"
        # })

    def clean(self, *args, **kwargs):
        #id = self.cleaned_data.get('business')
        name = self.cleaned_data.get("name")
        # publish = self.cleaned_data.get("publish")
        # phone = self.cleaned_data.get("phone")
        # address = self.cleaned_data.get("address")
        # url = self.cleaned_data.get("url")
        # logo = self.cleaned_data.get("logo")

        if not name or name == "":
            self.add_error("name", "Please enter a name for your business")

        return super(BusinessEditForm, self).clean(*args, **kwargs)

class BusinessCreateWizard(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Business Name</strong>"), required = False, max_length=50, min_length=1)
    phone = PhoneNumberField(label = "Phone Number", required = False, region="US")
    url = forms.URLField(label = "URL", help_text = "Enter a web address", max_length = 200, required = False)
    
    def __init__(self, *args, **kwargs):
        super(BusinessCreateWizard, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': "Business Name",
            'placeholder': "Name for your business"
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'name': "Phone Number"
        })
        # self.fields['address'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': "Address"
        # })
        self.fields['url'].widget.attrs.update({
            'class': 'form-control',
            'name': "URL"
        })
        # self.fields['logo'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': "Choose Logo"
        # })

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("name")

        if not name:
            self.add_error("name", "Please enter a name for your business")

        return super(BusinessCreateWizard, self).clean(*args, **kwargs)

class AddCurrencyWizard(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Campaign Name</strong>"), required = False, max_length=20, min_length=1)

    starts_at = forms.DateTimeField(label = 'Start Date', required = False, help_text = "Enter date as YYYY-MM-DD")
    ends_at = forms.DateTimeField(label = 'End Date', required = False)

    points_expire = forms.CharField(label = 'Points expire after', required = False, help_text = "Enter time(in days) that points will expire after")
    business = forms.ChoiceField(choices = [], help_text = "Choose a business")
    currency = forms.ChoiceField(choices=[], help_text = "Choose a currency")

    def __init__(self, *args, **kwargs):
        super(AddCurrencyWizard, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign Name',
            'placeholder': 'Enter a name for the campaign'
        })
        self.fields['starts_at'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Start Date'
        })
        self.fields['ends_at'].widget.attrs.update({
            'class': 'form-control',
            'name': 'End Date'
        })
        self.fields['points_expire'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Points Expiry Date'
        })
        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for biz in data.get('user').get('employee_of'):
            choices.append((biz.get('id'), biz.get('name')))
        self.initial['business'] = 'None'
        self.fields['business'] = forms.ChoiceField(choices=choices)
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name',
        })
        
        with open('currency.json', 'r') as f:
            currency = json.loads(f.read())
        choices = []
        for biz in currency.get('currency'):
            choices.append((biz.get('id'), biz.get('label')))
        self.initial['currency'] = 'None'
        self.fields['currency'] = forms.ChoiceField(choices=choices)
        self.fields['currency'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Currency Name',
        })
        self.fields['currency'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Currency ID'
        })

class AddCatalogWizard(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Catalog Name</strong>"),
                           max_length=20, min_length=1, required = False, help_text = "Choose a name for the catalog")
    
    business = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(AddCatalogWizard, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name',
            'placeholder': 'Category name'
        })

        with open('data.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for biz in data.get('user').get('employee_of'):
            choices.append((biz.get('id'), biz.get('name')))
        self.initial['business'] = 'None'
        self.fields['business'] = forms.ChoiceField(choices=choices)
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name',
        })

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("name")
        
        if not name:
            self.add_error('name', "Please enter a name")
        return super(AddCatalogWizard, self).clean(*args, **kwargs)
