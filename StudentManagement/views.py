from django.shortcuts import render, redirect
#
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect 
from django.http import HttpResponse 
from django.views.generic import View
import os
import subprocess
from django.db.models import Q
from subprocess import Popen

from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
#
from .forms import AlumnosForm, DocentesForm, CalificacionesForm, MateriasForm, GruposForm
from .models import alumnos, docentes, calificacion, materias, grupos
# Create your views here.
import MySQLdb 
connection = MySQLdb.connect("", "root", "", "studentsokoladli") 
#Creacion PDF
def render_pdf_view(request):
    materia = materias.objects.all()
    with connection.cursor() as cursor:
        cursor.callproc("reporteCalif")
        def dictfetchall(cursor):
            columns = [col[0] for col in cursor.description]
            return[
                dict(zip(columns,row))
                for row in cursor.fetchall()
            ]
        reportcalif=dictfetchall(cursor)
    for x in reportcalif:
        for y in materia:
            if x['claveMateria'] == y.claveMateria:
                x['claveMateria'] = y.nombreMateria
    #data = {'context',}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    # find the template and render it.
    template = get_template('pidief.html')
    html = template.render({'reportcalif': reportcalif})
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#Login------------------------------------------------------------------------------------
def inicio(request):
    if request.user.is_authenticated:
        return render(request, "modulo_menuSU.html")
    return render(request,"login.html")

def Login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('Menu')
            else:
                return redirect('invalido')
        else:
            return redirect('invalido')
    return render(request, "login.html", {'form': form})

def Logout(request):
    do_logout(request)
    return redirect('Login')

def invalido(request):
    return render(request,"nologin.html")

@login_required
def repetido(request):
    return render(request,"usuarioexistente.html")

#Menu
@login_required
def Menu(request):
    return render(request,'modulo_menuSU.html')

#Submenus
@login_required
def SubAlumno(request):
    return render(request,'SU_submenu_alumnos.html')
@login_required
def SubCalificaciones(request):
    return render(request,'SU_submenu_calificaciones.html')
@login_required
def SubGrupos(request):
    return render(request,'SU_submenu_grupos.html')
@login_required
def SubMaestro(request):
    return render(request,'SU_submenu_maestros.html')
@login_required
def SubMaterias(request):
    return render(request,'SU_submenu_materias.html')

#Contacto/Soporte
def Contacto(request):
    return render(request,'contacto.html')

def Soporte(request):
    return render(request,'soporte.html')

#Ver perfil
@login_required
def VerPerfil(request):
    return render(request,'perfil.html')

#Alumnos----------------------------------------------------------------------------------
@login_required
def AgregarAlumno(request):
    data2 = {'form':AlumnosForm}
    if request.method == 'POST':
        formulario = AlumnosForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('ConsultarAlumno')
        else:
            return redirect('repetido')
    return render(request, 'agregar_alumnosSU.html',data2)

@login_required
def Modificar_Alumno(request):
    busqueda = request.POST.get("buscar")
    alumno = alumnos.objects.all()
    if busqueda:
        alumno = alumnos.objects.filter(
            Q(matricula__icontains = busqueda) | 
            Q(nombre__icontains = busqueda) |
            Q(apellidoP__icontains = busqueda) |
            Q(apellidoM__icontains = busqueda) |
            Q(grado__icontains = busqueda) |
            Q(grupo__icontains = busqueda) |
            Q(nombreP__icontains = busqueda) 
        ).distinct()
    return render(request, 'modificarAlumno.html', {'alumno':alumno})

@login_required
def Eliminar_Alumno(request):
    busqueda = request.POST.get("buscar")
    alumno = alumnos.objects.all()
    if busqueda:
        alumno = alumnos.objects.filter(
            Q(matricula__icontains = busqueda) | 
            Q(nombre__icontains = busqueda) |
            Q(apellidoP__icontains = busqueda) |
            Q(apellidoM__icontains = busqueda) |
            Q(grado__icontains = busqueda) |
            Q(grupo__icontains = busqueda) 
        ).distinct()
    return render(request, 'eliminarAlumno.html', {'alumno':alumno})

@login_required
def ModificarAlumno(request,matricula):
    alumno = alumnos.objects.filter(matricula=matricula).first()
    if request.method == 'GET':
        form = AlumnosForm(instance= alumno)
    else:
        form = AlumnosForm(request.POST, instance= alumno)
        for x in alumnos.objects.all():
            if x.matricula == matricula:
                return redirect('repetido')
        if form.is_valid():
            form.save()
        else:
            return redirect('repetido')
        return redirect('ConsultarAlumno')
    return render(request,'modificar_alumnosSU.html',{'alumno': alumno})

@login_required
def EliminarAlumno(request,matricula):
    alumno = alumnos.objects.filter(matricula=matricula).first()
    if request.method == 'POST':
        alumno.delete()
        return redirect('ConsultarAlumno')
    return render(request,'eliminar_alumnosSU.html',{'alumno': alumno})

@login_required
def ConsultarAlumno(request):
    busqueda = request.POST.get("buscar")
    alumno = alumnos.objects.all()
    if busqueda:
        alumno = alumnos.objects.filter(
            Q(matricula__icontains = busqueda) | 
            Q(nombre__icontains = busqueda) |
            Q(apellidoP__icontains = busqueda) |
            Q(apellidoM__icontains = busqueda) |
            Q(grado__icontains = busqueda) |
            Q(grupo__icontains = busqueda) 
        ).distinct()
    return render(request, 'consultar_alumnos.html', {'alumno':alumno})

#Usuarios----------------------------------------------------------------------------------
@login_required
def AgregarUsuario(request):
    data2 = {'form':DocentesForm}
    if request.method == 'POST':
        formulario = DocentesForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('ConsultarUsuario')
        else:
            return redirect('repetido')
    return render(request, 'agregar_maestrosSU.html',data2)


@login_required
def Modificar_Usuario(request):
    busqueda = request.POST.get("buscar")
    docente = docentes.objects.all()
    if busqueda:
        docente = docentes.objects.filter(
            Q(claveDocente__icontains = busqueda) | 
            Q(password__icontains = busqueda) |
            Q(email__icontains = busqueda) |
            Q(curp__icontains = busqueda) |
            Q(nombre__icontains = busqueda) |
            Q(apellidoP__icontains = busqueda) |
            Q(apellidoM__icontains = busqueda)
        ).distinct()
    return render(request,'modificarUsuario.html', {'docente':docente})

@login_required
def Eliminar_Usuario(request):
    busqueda = request.POST.get("buscar")
    docente = docentes.objects.all()
    if busqueda:
        docente = docentes.objects.filter(
            Q(claveDocente__icontains = busqueda) | 
            Q(password__icontains = busqueda) |
            Q(email__icontains = busqueda) |
            Q(curp__icontains = busqueda) |
            Q(nombre__icontains = busqueda) |
            Q(apellidoP__icontains = busqueda) |
            Q(apellidoM__icontains = busqueda)
        ).distinct()
    return render(request,'eliminarUsuario.html', {'docente':docente})

@login_required
def ModificarUsuario(request,claveDocente):
    docente = docentes.objects.filter(claveDocente=claveDocente).first()
    if request.method == 'GET':
        form = DocentesForm(instance= docente)
    else:
        form = DocentesForm(request.POST, instance= docente)
        for x in docentes.objects.all():
            if x.claveDocente == claveDocente:
                return redirect('repetido')
        if form.is_valid():
            form.save()
        else:
            return redirect('repetido')
        return redirect('ConsultarUsuario')
    return render(request, 'modificar_maestro.html',{'docente': docente})

@login_required
def EliminarUsuario(request,claveDocente):
    docente = docentes.objects.filter(claveDocente=claveDocente).first()
    if request.method == 'POST':
        docente.delete()
        return redirect('ConsultarUsuario')
    return render(request, 'eliminar_maestro.html',{'docente': docente})

@login_required
def ConsultarUsuario(request):
    busqueda = request.POST.get("buscar")
    docente = docentes.objects.all()
    if busqueda:
        docente = docentes.objects.filter(
            Q(claveDocente__icontains = busqueda) | 
            Q(password__icontains = busqueda) |
            Q(email__icontains = busqueda) |
            Q(curp__icontains = busqueda) |
            Q(nombre__icontains = busqueda) |
            Q(apellidoP__icontains = busqueda) |
            Q(apellidoM__icontains = busqueda)
        ).distinct()
    return render(request,'consultar_maestro.html', {'docente':docente})

#Materias----------------------------------------------------------------------------------
@login_required
def AgregarMaterias(request):
    data2 = {'form':MateriasForm}
    if request.method == 'POST':
        formulario = MateriasForm(request.POST or None)
        if formulario.is_valid():
            data = formulario.cleaned_data 
            field = data['nombreMateria']
            for x in materias.objects.all():
                if field == x.nombreMateria:
                    return redirect('repetido')
                else:
                    formulario.save()
                    return redirect('ConsultarMaterias')
        else:
            return redirect('repetido')
    return render(request, 'agregar_materiasSU.html',data2)
     

@login_required
def Modificar_Materias(request):
    busqueda = request.POST.get("buscar")
    materia = materias.objects.all()
    if busqueda:
        materia = materias.objects.filter(
            Q(claveMateria__icontains = busqueda) | 
            Q(nombreMateria__icontains = busqueda) 
        ).distinct()
    return render(request,'modificarMaterias.html',{'materia': materia})

@login_required
def Eliminar_Materias(request):
    busqueda = request.POST.get("buscar")
    materia = materias.objects.all()
    if busqueda:
        materia = materias.objects.filter(
            Q(claveMateria__icontains = busqueda) | 
            Q(nombreMateria__icontains = busqueda) 
        ).distinct()
    return render(request,'eliminarMaterias.html',{'materia': materia})

@login_required
def ModificarMaterias(request,claveMateria):
    materia = materias.objects.filter(claveMateria=claveMateria).first()
    if request.method == 'GET':
        form = MateriasForm(instance= materia)
    else:
        form = MateriasForm(request.POST, instance= materia)
        if form.is_valid():
            data = form.cleaned_data 
            field = data['nombreMateria']
            for x in materias.objects.all():
                if x.claveMateria == claveMateria:
                    return redirect('repetido')
                else:
                    if field == x.nombreMateria:
                        return redirect('repetido')
                    else:
                        form.save()
        else:
            return redirect('repetido')
        return redirect('ConsultarMaterias')
    return render(request, 'modificar_materiasSU.html',{'materia': materia})

@login_required
def EliminarMaterias(request,claveMateria):
    materia = materias.objects.filter(claveMateria=claveMateria).first()
    if request.method == 'POST':
        materia.delete()
        return redirect('ConsultarMaterias')
    return render(request, 'eliminar_materiasSU.html',{'materia': materia})

@login_required
def ConsultarMaterias(request):
    busqueda = request.POST.get("buscar")
    materia = materias.objects.all()
    if busqueda:
        materia = materias.objects.filter(
            Q(claveMateria__icontains = busqueda) | 
            Q(nombreMateria__icontains = busqueda) 
        ).distinct()
    return render(request,'consultar_materias.html',{'materia': materia})

#Calificaciones----------------------------------------------------------------------------------
@login_required
def AgregarCalificaciones(request):
    data2 = {'form':CalificacionesForm}
    if request.method == 'POST':
        formulario = CalificacionesForm(request.POST or None)
        if formulario.is_valid():
            data = formulario.cleaned_data 
            field = data['matricula']
            field2 = data['claveMateria']
            for x in calificacion.objects.all():
                if field == x.matricula:
                    return redirect('repetido')
                else:
                    if field2 == x.claveMateria:
                        return redirect('repetido')
                    else:
                        formulario.save()
                        return redirect('ConsultarCalificaciones')
        else:
            return redirect('repetido') 
    return render(request, 'agregar_calificacionesSU.html',data2)

@login_required
def Modificar_Calificaciones(request):
    busqueda = request.POST.get("buscar")
    calificacione = calificacion.objects.all().order_by('matricula')
    if busqueda:
        calificacione = calificacion.objects.filter(
            #Q(incremento__icontains = busqueda) | 
            Q(matricula__matricula__icontains = busqueda) | 
            Q(claveMateria__claveMateria__icontains = busqueda) | 
            Q(calif__icontains = busqueda)|
            Q(estrategia__icontains = busqueda) 
        ).distinct()
    return render(request,'modificarCalificaciones.html',{'calificacione': calificacione})

@login_required
def Eliminar_Calificaciones(request):
    busqueda = request.POST.get("buscar")
    calificacione = calificacion.objects.all().order_by('matricula')
    if busqueda:
        calificacione = calificacion.objects.filter(
            #Q(incremento__icontains = busqueda) | 
            Q(matricula__matricula__icontains = busqueda) | 
            Q(claveMateria__claveMateria__icontains = busqueda) | 
            Q(calif__icontains = busqueda) |
            Q(estrategia__icontains = busqueda) 
        ).distinct()
    return render(request,'eliminarCalificaciones.html',{'calificacione': calificacione})

@login_required
def ModificarCalificaciones(request,incremento):
    calificacione = calificacion.objects.filter(incremento=incremento).first()
    if request.method == 'GET':
        form = CalificacionesForm(instance= calificacione)
    else:
        form = CalificacionesForm(request.POST, instance= calificacione)
        if form.is_valid():
            data = form.cleaned_data 
            field = data['matricula']
            field2 = data['claveMateria']
            for x in calificacion.objects.all():
                if field == x.matricula:
                    return redirect('repetido')
                else:
                    if field2 == x.claveMateria:
                        return redirect('repetido')
                    else:
                        form.save()
                        return redirect('ConsultarCalificaciones')
        else:
            return redirect('repetido') 
        return redirect('ConsultarCalificaciones')
    return render(request, 'modificar_calificacionesSU.html',{'calificacione': calificacione})

@login_required
def EliminarCalificaciones(request,incremento):
    calificacione = calificacion.objects.filter(incremento=incremento).first()
    if request.method == 'POST':
        calificacione.delete()
        return redirect('ConsultarCalificaciones')
    return render(request, 'eliminar_calificacionesSU.html',{'calificacione': calificacione})

@login_required
def ConsultarCalificaciones(request):
    busqueda = request.POST.get("buscar")
    calificacione = calificacion.objects.all().order_by('matricula')
    if busqueda:
        calificacione = calificacion.objects.filter(
            #Q(incremento__icontains = busqueda) | 
            Q(matricula__matricula__icontains = busqueda) | 
            Q(claveMateria__claveMateria__icontains = busqueda) |  
            Q(calif__icontains = busqueda) |
            Q(estrategia__icontains = busqueda) 
        ).distinct()
    return render(request,'consultar_calificaciones.html',{'calificacione': calificacione})


#Grupos----------------------------------------------------------------------------------
@login_required
def AgregarGrupos(request):
    data2 = {'form':GruposForm}
    if request.method == 'POST':
        formulario = GruposForm(request.POST or None)
        if formulario.is_valid():
            data = formulario.cleaned_data 
            field = data['claveGrupo']
            field2 = data['grupo']
            field3 = data['grado']
            for x in grupos.objects.all():
                if field == x.claveGrupo:
                    return redirect('repetido')
                else:
                    if field2 == x.grupo and field3 == x.grado:
                        return redirect('repetido')
                    else:
                        formulario.save()
                        return redirect('ConsultarGrupos')
        else:
            return redirect('repetido')
    return render(request, 'agregar_grupos.html',data2)
    
@login_required
def Modificar_Grupos(request):
    busqueda = request.POST.get("buscar")
    grupo = grupos.objects.all()
    if busqueda:
        grupo = grupos.objects.filter(
            Q(claveGrupo__icontains = busqueda) | 
            Q(grupo__icontains = busqueda) |
            Q(grado__icontains = busqueda) 
        ).distinct()
    return render(request,'modificarGrupos.html',{'grupo': grupo})

@login_required
def Eliminar_Grupos(request):
    busqueda = request.POST.get("buscar")
    grupo = grupos.objects.all()
    if busqueda:
        grupo = grupos.objects.filter(
            Q(claveGrupo__icontains = busqueda) |  
            Q(grupo__icontains = busqueda) |
            Q(grado__icontains = busqueda) 
        ).distinct()
    return render(request,'eliminarGrupos.html',{'grupo': grupo})

@login_required
def ModificarGrupos(request,claveGrupo):
    grupo = grupos.objects.filter(claveGrupo=claveGrupo).first()
    if request.method == 'GET':
        form = GruposForm(instance= grupo)
    else:
        form = GruposForm(request.POST, instance= grupo)
        if form.is_valid():
            data = form.cleaned_data 
            field = data['claveGrupo']
            field2 = data['grupo']
            field3 = data['grado']
            for x in grupos.objects.all():
                if field == x.claveGrupo:
                    return redirect('repetido')
                else:
                    if field2 == x.grupo and field3 == x.grado:
                        return redirect('repetido')
                    else:
                        form.save()
                        return redirect('ConsultarGrupos')
        else:
            return redirect('repetido')
        return redirect('ConsultarGrupos')
    return render(request, 'modificar_grupos.html',{'grupo': grupo})

@login_required
def EliminarGrupos(request,claveGrupo):
    grupo = grupos.objects.filter(claveGrupo=claveGrupo).first()
    if request.method == 'POST':
        grupo.delete()
        return redirect('ConsultarGrupos')
    return render(request, 'eliminar_grupos.html',{'grupo': grupo})

@login_required
def ConsultarGrupos(request):
    busqueda = request.POST.get("buscar")
    grupo = grupos.objects.all()
    if busqueda:
        grupo = grupos.objects.filter(
            Q(claveGrupo__icontains = busqueda) | 
            Q(grupo__icontains = busqueda) |
            Q(grado__icontains = busqueda) 
        ).distinct()
    return render(request,'consultar_grupos.html',{'grupo': grupo})