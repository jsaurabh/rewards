from django import forms
from django.utils.safestring import mark_safe
import json

class ItemViewForm(forms.Form):
    def __init__(self, categories, *args, **kwargs):
        super(ItemViewForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(
            choices = categories
        )

class AddCategoryForm(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Catalog Name</strong>"),
                           max_length=20, min_length=1, required = False, help_text = "Choose a name for the catalog")
    
    business = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
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
        return super(AddCategoryForm, self).clean(*args, **kwargs)

class DeleteCategoryForm(forms.Form):
    catalog_choice = forms.CharField(label='Catalog',
                           max_length=50, min_length=1)

    def __init__(self, *args, **kwargs):
        super(DeleteCategoryForm, self).__init__(*args, **kwargs)
        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
    
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['name']))

        self.initial['catalog_choice'] = 'None'
        self.fields['catalog_choice'] = forms.ChoiceField(choices=choices)
        self.fields['catalog_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

    
    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("id")
        return super(DeleteCategoryForm, self).clean(*args, **kwargs)

class EditCategoryForm(forms.Form):
    catalog_choice = forms.ChoiceField(choices=[])
    name = forms.CharField(label = mark_safe("<strong>*Catalog Name</strong>"),
                           max_length=20, min_length=1, required = False, help_text = "Choose a name for the catalog")
    
    business = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(EditCategoryForm, self).__init__(*args, **kwargs)

        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
        
        choices = []
        for choice in data:
            choices.append((choice['id'], choice['name']))

        self.initial['catalog_choice'] = 'None'
        self.fields['catalog_choice'] = forms.ChoiceField(choices=choices)
        self.fields['catalog_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

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
        return super(EditCategoryForm, self).clean(*args, **kwargs)


class AddItems(forms.Form):
    name = forms.CharField(label = mark_safe("<strong>*Item Name</strong>"),
                           max_length=50, min_length=1, required = False, help_text = "Enter name for the item")
    
    #image = forms.ImageField(allow_empty_file=True)
    category = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(AddItems, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name',
            'placeholder':'Item Name'
        })

        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Business Name'
        # })
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

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name'
        })

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("name")
        #image = self.cleaned_data.get("image")
        category = self.cleaned_data.get("category")

        if not name:
            self.add_error('name', 'Item name cannot be blank')
            
        return super(AddItems, self).clean(*args, **kwargs)

class EditItems(forms.Form):
    category = forms.ChoiceField(choices=[])
    item_choice = forms.ChoiceField(choices = [], label = mark_safe("<strong>Choose Item</strong>"))
    name = forms.CharField(label = mark_safe("<strong>*Item Name</strong>"),
                           max_length=50, min_length=1, required = False, help_text = "Enter name for the item")
    
    #image = forms.ImageField(allow_empty_file=True)
    

    def __init__(self, *args, **kwargs):
        super(EditItems, self).__init__(*args, **kwargs)
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

        print(choices)
        self.initial['item_choice'] = 'None'
        self.fields['item_choice'] = forms.ChoiceField(choices=choices)
        self.fields['item_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name',
            'placeholder':'Item Name'
        })

        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Business Name'
        # })


    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("name")
        #image = self.cleaned_data.get("image")
        category = self.cleaned_data.get("category")

        if not name:
            self.add_error('name', 'Item name cannot be blank')
            
        return super(EditItems, self).clean(*args, **kwargs)

class DeleteItems(forms.Form):
    item_choice = forms.CharField(label='Item ID',
                           max_length=50, min_length=1)

    def __init__(self, *args, **kwargs):
        super(DeleteItems, self).__init__(*args, **kwargs)
        with open('catalog.json', 'r') as f:
            data = json.loads(f.read())
        
        choices = []
        for choice in data:
            items = choice['items']
            for idx, item in enumerate(items):
                print(idx, item['id'], item['name'])
                choices.append((item['id'], item['name']))

        print(choices)
        self.initial['item_choice'] = 'None'
        self.fields['item_choice'] = forms.ChoiceField(choices=choices)
        self.fields['item_choice'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Catalog',
        })

    def clean(self, *args, **kwargs):
        item_choice = self.cleaned_data.get("id")
        return super(DeleteItems, self).clean(*args, **kwargs)