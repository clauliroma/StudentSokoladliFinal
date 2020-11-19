from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import alumnos,docentes, calificacion, materias, grupos

class AlumnosForm(forms.ModelForm):
    class Meta:
        model = alumnos
        fields= ['matricula','password','nombre','apellidoP','apellidoM','nombreP','grado','grupo',]

class DocentesForm(forms.ModelForm):
    class Meta:
        model = docentes
        fields= ['claveDocente','password','nombre','apellidoP','apellidoM','email','curp',]

class CalificacionesForm(forms.ModelForm):
    class Meta:
        model = calificacion
        fields= ['incremento','matricula','claveMateria','calif','estrategia',]

class MateriasForm(forms.ModelForm):
    class Meta:
        model = materias
        fields= ['claveMateria','nombreMateria',]

class GruposForm(forms.ModelForm):
    class Meta:
        model = grupos
        fields= ['claveGrupo','grado','grupo',]