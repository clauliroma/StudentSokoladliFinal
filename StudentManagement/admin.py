from django.contrib import admin
from .models import alumnos,docentes,grupos,materias,calificaciones

admin.site.register(alumnos)
admin.site.register(docentes)
admin.site.register(grupos)
admin.site.register(materias)
admin.site.register(calificaciones)
# Register your models here.
