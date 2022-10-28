# -*- encoding: utf-8 -*-
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myclasses.models import *




### logueo

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

#### Registro

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
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar contraseña",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

###### form agregar local 

class Boxform_add(forms.ModelForm):

    class Meta:
        model = Box
        fields = ('box', 'ubicacion', 'descripcion', 'logo')
        widgets = {
            'box' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gimnasio', 'autocomplete':'off'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicacion',  'autocomplete':'off'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 100, 'class': 'form-control', 'placeholder': 'Descripción', 'autocomplete':'off'}),
            
        }

        logo = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'type': 'file', 'id':'formFile', 'class': 'form-control'}))


    

    

    

