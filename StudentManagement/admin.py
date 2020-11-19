from django.contrib import admin
from .models import alumnos,docentes,grupos,materias,calificacion

admin.site.register(alumnos)
admin.site.register(docentes)
admin.site.register(grupos)
admin.site.register(materias)
admin.site.register(calificacion)
# Register your models here.
