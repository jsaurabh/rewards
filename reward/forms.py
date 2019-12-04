from django import forms
from django.utils.safestring import mark_safe
import json

class AddCampaignForm(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Campaign Name</strong>"), required = False, max_length=20, min_length=1)

    starts_at = forms.DateTimeField(label = 'Start Date', required = False)
    
    ends_at = forms.DateTimeField(label = 'End Date', required = False)

    points_expire = forms.CharField(label = 'Points expire after', required = False, help_text = "Enter time(in days) that points will expire after")
    business = forms.ChoiceField(choices = [], help_text = "Choose a business")
    currency = forms.ChoiceField(choices=[], help_text = "Choose a currency")

    def __init__(self, *args, **kwargs):
        super(AddCampaignForm, self).__init__(*args, **kwargs)
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

class DeleteCampaignForm(forms.Form):
    choose_campaign = forms.IntegerField(label = 'Campaign ID')

    def __init__(self, *args, **kwargs):
        super(DeleteCampaignForm, self).__init__(*args, **kwargs)
        with open('campaigns.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            #print(choice)
            choices.append((choice['id'], choice['name']))
        print(choices)
        self.initial['choose_campaign'] = 'None'
        self.fields['choose_campaign'] = forms.ChoiceField(choices=choices)
        self.fields['choose_campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Campaign',
        })

class EditCampaignForm(forms.Form):
    choose_campaign = forms.ChoiceField(choices=[])
    name = forms.CharField(label = mark_safe("<strong>*Campaign Name</strong>"), required = False, max_length=20, min_length=1)

    starts_at = forms.DateTimeField(label = 'Start Date', required = False)
    
    ends_at = forms.DateTimeField(label = 'End Date', required = False)

    points_expire = forms.CharField(label = 'Points expire after', required = False, help_text = "Enter time(in days) that points will expire after")
    business = forms.ChoiceField(choices = [], help_text = "Choose a business")
    currency = forms.ChoiceField(choices=[], help_text = "Choose a currency")

    def __init__(self, *args, **kwargs):
        super(EditCampaignForm, self).__init__(*args, **kwargs)
        
        with open('campaigns.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            #print(choice)
            choices.append((choice['id'], choice['name']))
        print(choices)
        self.initial['choose_campaign'] = 'None'
        self.fields['choose_campaign'] = forms.ChoiceField(choices=choices)
        self.fields['choose_campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Campaign',
        })
        
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



class AddCurrencyForm(forms.Form):
    label = forms.CharField(label = mark_safe("<strong>*Currency Name</strong>"),
                           max_length=20, min_length=1, required = False, help_text = "Choose a label for the currency")
    
    business = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(AddCurrencyForm, self).__init__(*args, **kwargs)
        self.fields['label'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Singular label',
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

class DeleteCurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(DeleteCurrencyForm, self).__init__(*args, **kwargs)
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

class EditCurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=[])    
    new_label = forms.CharField(label = mark_safe("<strong>*Currency Name</strong>"),
                           max_length=20, min_length=1, required = False, help_text = "Choose a label for the currency")
    business = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(EditCurrencyForm, self).__init__(*args, **kwargs)
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

class AddAccRulesForm(forms.Form):
    required_css_class = 'required'
    
    value = forms.IntegerField(label = mark_safe("<strong>Value</strong>"), max_value=4294967295, min_value=0)
    campaign = forms.ChoiceField(choices=[])
    category = forms.ChoiceField(choices=[])
    item = forms.ChoiceField(choices=[])
    # campaign = forms.IntegerField(label = mark_safe("<strong>*Campaign</strong>"), help_text = "Choose Campaign", required = False)
    # category = forms.IntegerField(label = mark_safe("<strong>*Category</strong>"), help_text = "Choose Category", required = False)
    # item = forms.IntegerField(label = mark_safe("<strong>*Item</strong>"), help_text = "Choose Item", required = False)

    def __init__(self, *args, **kwargs):
        super(AddAccRulesForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Value'
        })
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign ID'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Category ID'
        })
        self.fields['item'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Item'
        })

class EditAccRulesForm(forms.Form):
    value = forms.IntegerField(label = mark_safe("<strong>Value</strong>"), max_value=4294967295, min_value=0)
    campaign = forms.ChoiceField(choices=[])
    category = forms.ChoiceField(choices=[])
    item = forms.ChoiceField(choices=[])
    # campaign = forms.IntegerField(label = mark_safe("<strong>*Campaign</strong>"), help_text = "Choose Campaign", required = False)
    # category = forms.IntegerField(label = mark_safe("<strong>*Category</strong>"), help_text = "Choose Category", required = False)
    # item = forms.IntegerField(label = mark_safe("<strong>*Item</strong>"), help_text = "Choose Item", required = False)

    def __init__(self, *args, **kwargs):
        super(EditAccRulesForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Value'
        })
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign ID'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Category ID'
        })
        self.fields['item'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Item'
        })

class DeleteAccRulesForm(forms.Form):
    Rule = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super(DeleteAccRulesForm, self).__init__(*args, **kwargs)
        self.fields['Rule'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule ID'
        })

class AddRedRulesForm(forms.Form):

    reward = forms.CharField(label = 'Reward', max_length=20, min_length=1)
    #image = forms.ImageField(label = 'Image')
    value = forms.IntegerField(label = 'Value', max_value= 4294967295, min_value=0)
    campaign = forms.IntegerField(label = 'Campaign', )

    def __init__(self, *args, **kwargs):
        super(AddRedRulesForm, self).__init__(*args, **kwargs)

        self.fields['reward'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Reward ID'
        })
        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Image'
        # })
        self.fields['value'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Value'
        })
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign ID'
        })

class EditRedRulesForm(forms.Form):
    id = forms.IntegerField(label = "ID")
    reward = forms.CharField(label = 'Reward', max_length=20, min_length=1)
    #image = forms.ImageField(label = 'Image')
    value = forms.IntegerField(label = 'Value', max_value= 4294967295, min_value=0)
    campaign = forms.IntegerField(label = 'Campaign', )

    def __init__(self, *args, **kwargs):
        super(EditRedRulesForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule ID'
        })
        self.fields['reward'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Reward ID'
        })
        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Image'
        # })
        self.fields['value'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Value'
        })
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign ID'
        })

class DeleteRedRulesForm(forms.Form):
    Rule = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super(DeleteRedRulesForm, self).__init__(*args, **kwargs)
        self.fields['Rule'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule ID'
        })
        