# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myclasses.models import *
from utilidades import formularios
from django.forms import PasswordInput
from django.core import validators


### logueo

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

class SignUpForm(UserCreationForm):
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
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

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

####fin##

#### planes ###

class Planform_add(forms.ModelForm):

    class Meta:
        model = Planes
        fields = ('titulo', 'disciplina', 'horario','precio', 'cantidad_clases')
        widgets = {
            'titulo' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo', 'autocomplete':'off'}),            
            'disciplina' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disciplina', 'autocomplete':'off'}),            
            'precio' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'onkeypress': 'return soloNumeros(event)', 'autocomplete':'off'}),
            'cantidad_clases': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad de clases', 'type': 'number', 'autocomplete':'off'}),
                   
            
        }
        
####fin##

### clases ####


class Clasesform_add(forms.ModelForm):

    class Meta:
        model = Clases
        fields = ('descripcion','inicioClase','terminoClase', 'duracion','modalidad', 'cupo')
        widgets = {
            'descripcion' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'autocomplete':'off'}),            
            'inicioClase' : forms.TimeInput(format='%h:%M', attrs={'class': 'form-control', 'placeholder': 'Inicio de clases','type': 'time', 'autocomplete':'off'}),
            'terminoClase' : forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Termino de clases','type': 'time', 'autocomplete':'off'}),            
            'duracion' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duracion de la clase','type': 'number',  'autocomplete':'off'}),            
            'cupo' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'maximo de cupos', 'type': 'number', 'onkeypress': 'return soloNumeros(event)', 'autocomplete':'off'}),            
                   
            
        }
       
        
    ####fin ##

    ## reservas #
    
class Reservaform_add(forms.Form):
    clase = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control ' }), choices=formularios.get_clases_choices)        
    estado = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={' class': 'f  ss','checked':'true' }))
    
 
	

    

    

    

