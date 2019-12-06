from django import forms
from django.utils.safestring import mark_safe
import json
from bootstrap_datepicker_plus import DatePickerInput

class AddCampaignForm(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Campaign Name</strong>"), required = False, max_length=20, min_length=1)

    starts_at = forms.DateTimeField(label = 'Start Date', required = False, widget = DatePickerInput(format='%m/%d/%Y'))
    
    ends_at = forms.DateTimeField(label = 'End Date', required = False, widget = DatePickerInput(format='%m/%d/%Y'))

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
        # self.fields['starts_at'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Start Date'
        # })
        # self.fields['ends_at'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'End Date'
        # })
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

    starts_at = forms.DateTimeField(label = 'Start Date', required = False, widget = DatePickerInput(format='%m/%d/%Y'))
    
    ends_at = forms.DateTimeField(label = 'End Date', required = False, widget = DatePickerInput(format='%m/%d/%Y'))

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

    value = forms.IntegerField(label = mark_safe("<strong>Value</strong>"), max_value=4294967295, min_value=0)
    campaign = forms.ChoiceField(choices=[])
    CHOICES = [('C', 'Category'), ('I', 'Item')]

    category = forms.ChoiceField(choices=[], help_text = "Choose either one of category or item to apply the rule to", required = False)
    item = forms.ChoiceField(choices=[], required = False)
    
    rule = forms.ChoiceField(label = mark_safe("Rule Scope"), choices = CHOICES, help_text = "Determines what level the rules are applied at")
    
    def __init__(self, *args, **kwargs):
        super(AddAccRulesForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Value'
        })
        with open('campaigns.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            #print(choice)
            choices.append((choice['id'], choice['name']))
        self.initial['campaign'] = 'None'
        self.fields['campaign'] = forms.ChoiceField(choices=choices)
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Campaign',
        })

        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
        
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['name']))

        self.initial['category'] = 'None'
        self.fields['category'] = forms.ChoiceField(choices=choices)
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
        
        choices = []
        for choice in data:
            items = choice['items']
            for idx, item in enumerate(items):
                print(idx, item['id'], item['name'])
                choices.append((item['id'], item['name']))

        self.initial['item'] = 'None'
        self.fields['item'] = forms.ChoiceField(choices=choices)
        self.fields['item'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

        self.fields['rule'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule Choice'
        })

    def clean(self, *args, **kwargs):
        value = self.cleaned_data.get("value")
        choice = self.cleaned_data.get("rule")
        category = self.cleaned_data.get("category")
        item = self.cleaned_data.get("item")
        
        if choice == "C":
            item = None
        else:
            category = None
        if not value:
            self.add_error('value', "Value cannot be blank")

        return super(AddAccRulesForm, self).clean(*args, **kwargs)

class EditAccRulesForm(forms.Form):
    campaign = forms.ChoiceField(choices=[])
    category = forms.ChoiceField(choices=[], help_text = "Choose either one of category or item to apply the rule to", required = False)
    item = forms.ChoiceField(choices=[], required = False)
    
    rule_choice = forms.ChoiceField(choices=[], label = mark_safe("<strong>Choose Rule</strong>"),)
    value = forms.IntegerField(label = mark_safe("<strong>Value</strong>"), max_value=4294967295, min_value=0)
    
    CHOICES = [('C', 'Category'), ('I', 'Item')]

    
    rule = forms.ChoiceField(label = mark_safe("Rule Scope"), choices = CHOICES, help_text = "Determines what level the rules are applied at")
    
    def __init__(self, *args, **kwargs):
        super(EditAccRulesForm, self).__init__(*args, **kwargs)

        self.fields['value'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Value'
        })
        with open('campaigns.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['name']))
        self.initial['campaign'] = 'None'
        self.fields['campaign'] = forms.ChoiceField(choices=choices)
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Campaign',
        })

        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
        
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['name']))

        self.initial['category'] = 'None'
        self.fields['category'] = forms.ChoiceField(choices=choices)
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
        
        choices = []
        for choice in data:
            items = choice['items']
            for idx, item in enumerate(items):
                print(idx, item['id'], item['name'])
                choices.append((item['id'], item['name']))

        self.initial['item'] = 'None'
        self.fields['item'] = forms.ChoiceField(choices=choices)
        self.fields['item'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

        with open('rules.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['value']))
        self.initial['rule_choice'] = 'None'
        self.fields['rule_choice'] = forms.ChoiceField(choices=choices)
        self.fields['rule_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Value',
        })

        self.fields['rule'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule Choice'
        })

    def clean(self, *args, **kwargs):
        value = self.cleaned_data.get("value")
        choice = self.cleaned_data.get("rule")
        category = self.cleaned_data.get("category")
        item = self.cleaned_data.get("item")
        
        if choice == "C":
            item = None
        else:
            category = None
        if not value:
            self.add_error('value', "Value cannot be blank")

        return super(EditAccRulesForm, self).clean(*args, **kwargs)

class DeleteAccRulesForm(forms.Form):
    rule_choice = forms.ChoiceField(choices=[], label = mark_safe("<strong>Choose Rule</strong>"))
    
    def __init__(self, *args, **kwargs):
        super(DeleteAccRulesForm, self).__init__(*args, **kwargs)
        with open('rules.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['value']))
        self.initial['rule_choice'] = 'None'
        self.fields['rule_choice'] = forms.ChoiceField(choices=choices)
        self.fields['rule_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Value',
        })

class AddRedRulesForm(forms.Form):

    reward = forms.CharField(label = mark_safe("<strong>Reward</strong>"), max_length=20, min_length=1, required = False, help_text = "Brief description of the reward")
    value = forms.IntegerField(label = mark_safe("<strong>Value</strong>"), max_value=4294967295, min_value=0, required = False)
    campaign = forms.ChoiceField(choices=[], required = False)
    #image = forms.ImageField(label = 'Image')
    
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
        with open('campaigns.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            #print(choice)
            choices.append((choice['id'], choice['name']))
        self.initial['campaign'] = 'None'
        self.fields['campaign'] = forms.ChoiceField(choices=choices)
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Campaign',
        })

    def clean(self, *args, **kwargs):
        reward = self.cleaned_data.get('reward')

        if not reward:
            self.add_error("reward", "Reward cannot be left blank")

class EditRedRulesForm(forms.Form):
    campaign = forms.ChoiceField(choices=[], required = False)
    reward_choice = forms.ChoiceField(choices = [], help_text = "Choose existing reward to modify")
    reward = forms.CharField(label = mark_safe("<strong>Reward</strong>"), max_length=20, min_length=1, required = False, help_text = "Brief description of the reward")
    value = forms.IntegerField(label = mark_safe("<strong>Value</strong>"), max_value=4294967295, min_value=0, required = False)
    #image = forms.ImageField(label = 'Image')
    
    def __init__(self, *args, **kwargs):
        super(EditRedRulesForm, self).__init__(*args, **kwargs)

        with open('campaigns.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['name']))
        self.initial['campaign'] = 'None'
        self.fields['campaign'] = forms.ChoiceField(choices=choices)
        self.fields['campaign'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Campaign',
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

        with open('redRules.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            print(choice)
            choices.append((choice['id'], choice['value']))
        self.initial['reward_choice'] = 'None'
        self.fields['reward_choice'] = forms.ChoiceField(choices=choices)
        self.fields['reward_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Existig Reward',
        })

    def clean(self, *args, **kwargs):
        reward = self.cleaned_data.get('reward')

        if not reward:
            self.add_error("reward", "Reward cannot be left blank")

class DeleteRedRulesForm(forms.Form):
    rule_choice = forms.ChoiceField(choices = [], label = mark_safe("<strong>Choose Rule</strong>"), required = False)
    
    def __init__(self, *args, **kwargs):
        super(DeleteRedRulesForm, self).__init__(*args, **kwargs)
        
        with open('redRules.json', 'r') as f:
            data = json.loads(f.read())
        choices = []
        for choice in data:
            print(choice)
            choices.append((choice['id'], choice['value']))
        self.initial['rule_choice'] = 'None'
        self.fields['rule_choice'] = forms.ChoiceField(choices=choices)
        self.fields['rule_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Choose Rule',
        })
        