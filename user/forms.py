from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={"class":"form-control"}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(max_length=25, widget= forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs= {"class":"form-control"}), label="Şifre")
    password2 = forms.CharField(widget = forms.PasswordInput(attrs= {"class":"form-control"}), label="Şifre Tekrar")


    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name","password1","password2")
