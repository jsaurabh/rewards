from django.contrib.auth import authenticate
from django import forms

class UsersLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput,)

	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Username"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Password"})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Enter valid info")

		return super(UsersLoginForm, self).clean(*args, **keyargs)

class UsersRegistrationForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput, )
	first_Name = forms.CharField()
	last_Name = forms.CharField()
	email = forms.EmailField()
	phone = forms.CharField(max_length=10, min_length=10)

	def __init__(self, *args, **kwargs):
		super(UsersRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
			'class': 'form-control',
			'name':"Username"
		})
		self.fields['password'].widget.attrs.update({
			'class': 'form-control',
			'name':"Password"
		})
		self.fields['first_Name'].widget.attrs.update({
			'class': 'form-control',
			'name':"First "
		})
		self.fields['last_Name'].widget.attrs.update({
			'class': 'form-control',
			'name':"Last Name"
		})
		self.fields['email'].widget.attrs.update({
			'class': 'form-control',
			'name':"Email"
		})
		self.fields['phone'].widget.attrs.update({
			'class': 'form-control',
			'name':"Phone Number"
		})

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		firstName = self.cleaned_data.get("firstName")
		lastName = self.cleaned_data.get("lastName")
		email = self.cleaned_data.get("email")
		phone = self.cleaned_data.get("phone")

		return super(UsersRegistrationForm, self).clean(*args, **kwargs)

