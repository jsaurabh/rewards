from django import forms

class AddCampaignForm(forms.Form):
    name = forms.CharField(label='Name',
                           max_length=20, min_length=1)

    starts_at = forms.DateTimeField(label = 'Start Date')
    
    ends_at = forms.DateTimeField(label = 'End Date')

    points_expire = forms.IntegerField(label = 'Points expire after')
    business = forms.IntegerField(label = 'Business ID')
    currency = forms.IntegerField(label = 'Currency ID')

    def __init__(self, *args, **kwargs):
        super(AddCampaignForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign Name'
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
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business ID'
        })
        self.fields['currency'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Currency ID'
        })

class DeleteCampaignForm(forms.Form):
    id = forms.IntegerField(label = 'Campaign ID')

    def __init__(self, *args, **kwargs):
        super(DeleteCampaignForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign ID'
        })

class EditCampaignForm(forms.Form):
    id = forms.IntegerField(label = 'Campaign ID')
    
    name = forms.CharField(label='Name',
                           max_length=20, min_length=1)

    starts_at = forms.DateTimeField(label = 'Start Date')
    
    ends_at = forms.DateTimeField(label = 'End Date')

    points_expire = forms.IntegerField(label = 'Points expire after')
    business = forms.IntegerField(label = 'Business ID')
    currency = forms.IntegerField(label = 'Currency ID')

    def __init__(self, *args, **kwargs):
        super(EditCampaignForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign ID'
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Campaign Name'
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
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business ID'
        })
        self.fields['currency'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Currency ID'
        })

class AddCurrencyForm(forms.Form):
    singular_label = forms.CharField(label='Singular Label',
                           max_length=20, min_length=1)

    plural_label = forms.CharField(label = 'Plural Label', 
                            max_length=20, min_length=1)
    
    business = forms.IntegerField(label = 'Business ID')

    def __init__(self, *args, **kwargs):
        super(AddCurrencyForm, self).__init__(*args, **kwargs)
        self.fields['singular_label'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Singular label'
        })
        self.fields['plural_label'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Plural label'
        })
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business ID'
        })

        # def clean(self, *args, **kwargs):
        #     name = self.cleaned_data.get("name")
        #     name = self.cleaned_data.get("name")
        #     name = self.cleaned_data.get("name")
        #     return super(AddCurrencyForm, self).clean(*args, **kwargs)

class DeleteCurrencyForm(forms.Form):
    id = forms.IntegerField(label = 'Currency ID')

    def __init__(self, *args, **kwargs):
        super(DeleteCurrencyForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Currency ID'
        })

class EditCurrencyForm(forms.Form):
    id = forms.IntegerField(label = 'Currency ID')

    singular_label = forms.CharField(label='Singular Label',
                           max_length=20, min_length=1)

    plural_label = forms.CharField(label = 'Plural Label', 
                            max_length=20, min_length=1)
    
    business = forms.IntegerField(label = 'Business ID')

    def __init__(self, *args, **kwargs):
        super(EditCurrencyForm, self).__init__(*args, **kwargs)

        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Currency ID'
        })
        self.fields['singular_label'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Singular label'
        })
        self.fields['plural_label'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Plural label'
        })
        self.fields['business'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business ID'
        })

class AddAccRulesForm(forms.Form):
    # id = forms.IntegerField(label = "ID")
    value = forms.IntegerField(label = 'Value', max_value=4294967295, min_value=0)
    campaign = forms.IntegerField(label = 'Campaign ID')
    category = forms.CharField(label = 'Category ID', required = False)
    item = forms.CharField(label = 'Item', required = False)

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
    id = forms.IntegerField(label = "Rule ID")
    value = forms.IntegerField(label = 'Value')
    campaign = forms.IntegerField(label = 'Campaign ID')
    category = forms.CharField(required = False, label = 'Category ID')
    item = forms.CharField(required = False, label = 'Value')

    def __init__(self, *args, **kwargs):
        super(EditAccRulesForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule ID'
        })
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
    id = forms.IntegerField(label = "Rule ID")
    
    def __init__(self, *args, **kwargs):
        super(DeleteAccRulesForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
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
    id = forms.IntegerField(label = "ID")

    def __init__(self, *args, **kwargs):
        super(DeleteRedRulesForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Rule ID'
        })
        