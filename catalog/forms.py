from django import forms

class ItemViewForm(forms.Form):
    def __init__(self, categories, *args, **kwargs):
        super(ItemViewForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(
            choices = categories
        )

class AddCategoryForm(forms.Form):
    name = forms.CharField(label='Category Name',
                           max_length=50, min_length=1)

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name'
        })

        def clean(self, *args, **kwargs):
            name = self.cleaned_data.get("name")
            return super(AddCategoryForm, self).clean(*args, **kwargs)

class DeleteCategoryForm(forms.Form):
    id = forms.CharField(label='Category ID',
                           max_length=50, min_length=1)

    def __init__(self, *args, **kwargs):
        super(DeleteCategoryForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Category ID'
        })

        def clean(self, *args, **kwargs):
            name = self.cleaned_data.get("id")
            return super(DeleteCategoryForm, self).clean(*args, **kwargs)

class EditCategoryForm(forms.Form):
    name = forms.CharField(label='Category Name',
                           max_length=50, min_length=1)
    id = forms.CharField(label = "Unique identifier")
    def __init__(self, *args, **kwargs):
        super(EditCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name'
        })
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': "Category ID"
        })

        def clean(self, *args, **kwargs):
            name = self.cleaned_data.get("name")
            id = self.cleaned_data.get('id')

            return super(EditCategoryForm, self).clean(*args, **kwargs)

class AddItems(forms.Form):
    name = forms.CharField(label='Item Name',
                           max_length=50, min_length=1)
    #image = forms.ImageField(allow_empty_file=True)
    category = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(AddItems, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name'
        })
        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Business Name'
        # })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Business Name'
        })

        def clean(self, *args, **kwargs):
            name = self.cleaned_data.get("name")
            #image = self.cleaned_data.get("image")
            category = self.cleaned_data.get("category")
            return super(AddItems, self).clean(*args, **kwargs)

class EditItems(forms.Form):
    id = forms.IntegerField(label='Item ID')
    name = forms.CharField(label='Item Name',
                           max_length=50, min_length=1)
    #image = forms.ImageField(allow_empty_file=True)
    category = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(EditItems, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Item ID'
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Item Name'
        })
        # self.fields['image'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'Item image'
        # })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Item Category_ID'
        })

        def clean(self, *args, **kwargs):
            id = self.cleaned_data.get("id")
            name = self.cleaned_data.get("name")
            #image = self.cleaned_data.get("image")
            category = self.cleaned_data.get("category")
            return super(EditItems, self).clean(*args, **kwargs)

class DeleteItems(forms.Form):
    id = forms.CharField(label='Item ID',
                           max_length=50, min_length=1)

    def __init__(self, *args, **kwargs):
        super(DeleteItems, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({
            'class': 'form-control',
            'name': 'Item ID'
        })

        def clean(self, *args, **kwargs):
            id = self.cleaned_data.get("id")
            return super(DeleteItems, self).clean(*args, **kwargs)