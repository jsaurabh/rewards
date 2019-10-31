from django.contrib.auth import authenticate
from django import forms

class UsersLoginForm(forms.Form):
	account_number = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput,)

	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['account_number'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Account Number"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Password"})

	def clean(self, *args, **keyargs):
		account = self.cleaned_data.get("account_number")
		password = self.cleaned_data.get("password")
		
		if account and password:
			user = authenticate(username = account, password = password)
			if not user:
				raise forms.ValidationError("Enter valid account data")

		return super(UsersLoginForm, self).clean(*args, **keyargs)
 

class UsersRegistrationForm(forms.Form):
	pass

