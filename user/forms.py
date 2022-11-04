# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from utilidades import formularios
from django.forms import PasswordInput
from django.core import validators

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                'autocomplete':'off'
            }
        ),
        validators=[
                validators.MinLengthValidator(4, message="El E-Mail es demasiado corto"),
				validators.RegexValidator('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="El E-Mail ingresado no es válido")
        ],
                error_messages={'required':'El campo E-Mail está vacío' }
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))

#### Registro

class registroForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
                'autocomplete':'off'
            }
        ),
        validators=[
                validators.MinLengthValidator(4, message="El E-Mail es demasiado corto"),
				validators.RegexValidator('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="El E-Mail ingresado no es válido")
        ],
                error_messages={'required':'El campo E-Mail está vacío' }
        )
    
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre' }))
    
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))

    comunidad = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control '}), choices=formularios.get_box_choices)
    
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
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')



### reserva ##

class Reservaform_user(forms.Form):        
    cupo_reservado = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reservar' }))