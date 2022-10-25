# -*- encoding: utf-8 -*-
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myclasses.models import *



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




class Boxform_add(forms.ModelForm):

    class Meta:
        model = Box
        fields = ('box', 'ubicacion', 'descripcion','logo')
        widgets = {
            'box' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gymnasio', 'autocomplete':'off'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicacion',  'autocomplete':'off'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 100, 'class': 'form-control', 'placeholder': 'Descripción', 'autocomplete':'off'}),
            'logo': forms.TextInput(attrs={ 'type': 'file', 'id':'formFile', 'class': 'form-control'}),
        }




    

    

    

