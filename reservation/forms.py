from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking

# Booking form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # No additional fields since user and flight are set in view

# User registration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Login form (optional if using Django's built-in auth views)
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
