from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.utils.safestring import mark_safe

class UsersLoginForm(forms.Form):
	username = forms.CharField(label = mark_safe("<strong>*Username</strong>"), required = False, max_length=150, min_length=1)
	password = forms.CharField(label = mark_safe("<strong>*Password</strong>"), required = False, widget = forms.PasswordInput())

	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control text-light',
		    "name":"Username",
			'placeholder': "Enter username"
			})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"Password",
			"placeholder": "Enter password"
			})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if not username and not password:
			self.add_error(None, "Please fill out the form")
		elif not username:
			self.add_error("username", "Please enter a username")
		elif not password:
			self.add_error("password", "Please enter the password")
			
		return super(UsersLoginForm, self).clean(*args, **keyargs)

class UsersRegistrationForm(forms.Form):
	# error_css_class = 'error'
	required_css_class = 'required'
	username = forms.CharField(label = mark_safe("<strong>*Username</strong>"), required = False, max_length=150, min_length=3)
	password = forms.CharField(label = mark_safe("<strong>*Password</strong>"), required = False, help_text = "8 characters or more", widget = forms.PasswordInput())
	confirm_password = forms.CharField(label = mark_safe("<strong>*Confirm Password</strong>"), required = False, widget = forms.PasswordInput())
	first_Name = forms.CharField(label = "First Name", required = False, max_length=30)
	last_Name = forms.CharField(label = "Last Name", required = False, max_length=150)
	email = forms.EmailField(required = False, max_length = 254)
	phone = PhoneNumberField(label = "Phone Number", required = False, region="US")

	def __init__(self, *args, **kwargs):
		super(UsersRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username']
		self.fields['username'].widget.attrs.update({
			'class': 'form-control text-light',
			'name':"Username",
			'placeholder': 'Choose username',
		})
		self.fields['password'].widget.attrs.update({
			'class': 'form-control',
			'name':"Password",
			'placeholder': 'Choose password'
		})
		self.fields['confirm_password'].widget.attrs.update({
			'class': 'form-control',
			'name':"Password",
			'placeholder': 'Enter password again',
		})
		self.fields['first_Name'].widget.attrs.update({
			'class': 'form-control',
			'name':"First Name"
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
			'name':'Phone Number', 
			'placeholder': 'Enter phone number'
		})

	def clean(self, *args, **kwargs):
		
		cleaned_data = super(UsersRegistrationForm, self).clean()
		name = cleaned_data.get('username')
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		fName = cleaned_data.get('first_Name')
		lName = cleaned_data.get('last_Name')
		phone = cleaned_data.get('phone')
		email = cleaned_data.get('email')

		labels = {
			'username': 'Username', 
			'password' : 'Password',
			'confirm_password': "Comfirm Password"
		}

		if not name and not password and not confirm_password:
			self.add_error(None, "Please fill out the form")


		elif not name or not password or not confirm_password:
			noinput = []
			if not name:
				noinput.append("username")
			if not password:
				noinput.append("password")
			if not confirm_password:
				noinput.append("confirm_password")
			print(noinput)
			for item in noinput:
				self.add_error(item, "{0} cannot be blank".format(labels[item]))

		elif name and password and confirm_password:
			if password != confirm_password:
				self.add_error("password", "Passwords do not match")
			# else:
		# 	if not name:
		# 		self.add_error("username", "Username cannot be blank")
		# 	elif not confirm_password and not password:
		# 		self.add_error("confirm_password", "Confrim password cannot be blank")
		# 		self.add_error("password", "Password cannot be blank")
		# 	elif not password:
		# 		self.add_error("password", "Password cannot be blank")


		# elif not name:
		# 	self.add_error("username", "Username cannot be empty")
		# 	if not password:
		# 		self.add_error("password", "Password cannot be empty")
		# 	if not confirm_password:
		# 		self.add_error("confirm_password", "Confirm Password cannot be empty")
		# 	if password != confirm_password:
		# 		self.add_error("password", "Passwords do not match. Please enter the same password")
		# elif not password:
		# 	self.add_error("password", "Password cannot be empty")
		# 	if confirm_password:
		# 		self.add_error("confirm_password", "Password needs to entered")
		
		# else:
		# 	if password != confirm_password:
		# 		self.add_error("password", "Passwords do not match. Please enter the same password")
			# if not password:
			# 	self.add_error("password", "Password cannot be empty")
			# if not confirm_password:
			# 	self.add_error("confirm_password", "Confirm Password cannot be empty")
			
		# firstName = cleaned_data.get("firstName")
		# lastName = cleaned_data.get("lastName")
		# email = cleaned_data.get("email")
		# phone = self.cleaned_data.get("phone")

		return super(UsersRegistrationForm, self).clean(*args, **kwargs)

			# if not fName:
			# 	self.add_error("first_Name", "First Name cannot be empty")
			# if not lName:
			# 	self.add_error("last_Name", "Last Name cannot be empty")
			# if not phone:
			# 	self.add_error("phone", "Phone Number cannot be empty")
			# if not email:
			# 	self.add_error("email", "Email cannot be empty")