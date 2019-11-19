from django import forms


class BusinessCreationForm(forms.Form):
    name = forms.CharField(label='Business Name',
                           max_length=50, min_length=1)
    #publish = forms.ChoiceField(choices = ['Yes', 'No'], widget = forms.RadioSelect())
    phone = forms.CharField(max_length=16)
    url = forms.URLField()
    address = forms.CharField()
   # logo = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(BusinessCreationForm, self).__init__(*args, **kwargs)
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
            name = self.cleaned_data.get("name")
            #publish = self.cleaned_data.get("publish")
            phone = self.cleaned_data.get("phone")
            address = self.cleaned_data.get("address")
            url = self.cleaned_data.get("url")
            #logo = self.cleaned_data.get("logo")

            return super(BusinessCreationForm, self).clean(*args, **kwargs)

class BusinessEditForm(forms.Form):
    id = forms.CharField(label = "Unique identifier")
    name = forms.CharField(label='Business Name',
                           max_length=50, min_length=1)
    #publish = forms.ChoiceField(choices = ['Yes', 'No'], widget = forms.RadioSelect())
    phone = forms.CharField(max_length=16)
    url = forms.URLField()
    address = forms.CharField()
   # logo = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(BusinessEditForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
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
            id = self.cleaned_data.get('id')
            name = self.cleaned_data.get("name")
            #publish = self.cleaned_data.get("publish")
            phone = self.cleaned_data.get("phone")
            address = self.cleaned_data.get("address")
            url = self.cleaned_data.get("url")
            #logo = self.cleaned_data.get("logo")

            return super(BusinessEditForm, self).clean(*args, **kwargs)
