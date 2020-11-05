from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import logout_then_login
from django.conf.urls.static import static
from .views import repetido,Eliminar_Grupos,Modificar_Grupos,Eliminar_Materias,Modificar_Materias,Eliminar_Calificaciones,Modificar_Calificaciones,Modificar_Usuario,Eliminar_Usuario,Eliminar_Alumno,Modificar_Alumno,VerPerfil,Logout,invalido,Soporte, Contacto, ConsultarMaterias,ConsultarGrupos,ConsultarCalificaciones,ConsultarUsuario,ConsultarAlumno,AgregarGrupos, ModificarGrupos, EliminarGrupos, SubAlumno, SubCalificaciones, SubMaterias, SubMaestro, SubGrupos , Login, Menu, AgregarAlumno, AgregarUsuario, AgregarCalificaciones, AgregarMaterias,ModificarAlumno,ModificarUsuario,ModificarCalificaciones,ModificarMaterias,EliminarAlumno, EliminarUsuario, EliminarMaterias, EliminarCalificaciones

urlpatterns = [
    #Login
    path('Login',Login,name='Login'),
    path('Logout',Logout,name='Logout'),
    path('invalido',invalido,name='invalido'),
    path('repetido',repetido,name='repetido'),
    # Menú
    path('Menu',Menu,name='Menu'),
    # Contacto
    path('Contacto',Contacto,name='Contacto'),
    # Soporte
    path('Soporte',Soporte,name='Soporte'),
    #Ver perfil
    path('VerPerfil',VerPerfil,name='VerPerfil'),
    #Submenus
    path('Alumno',SubAlumno,name='SubAlumno'),
    path('Maestro',SubMaestro,name='SubMaestro'),
    path('Calificaciones',SubCalificaciones,name='SubCalificaciones'),
    path('Grupos',SubGrupos,name='SubGrupos'),
    path('Materias',SubMaterias,name='SubMaterias'),
    #Alumnos
    path('AgregarAlumno',AgregarAlumno,name='AgregarAlumno'),
    path('ModificarAlumno',Modificar_Alumno,name='Modificar_Alumno'),
    path('EliminarAlumno',Eliminar_Alumno,name='Eliminar_Alumno'),
    path('ConsultarAlumno',ConsultarAlumno,name='ConsultarAlumno'),
    path(r'^update/(?P<matricula>\d+)/',ModificarAlumno,name='ModificarAlumno'),
    path(r'^delete/(?P<matricula>\d+)/',EliminarAlumno,name='EliminarAlumno'),

    #Usuarios
    path('AgregarUsuario',AgregarUsuario,name='AgregarUsuario'),
    path('ModificarUsuario',Modificar_Usuario,name='Modificar_Usuario'),
    path('EliminarUsuario',Eliminar_Usuario,name='Eliminar_Usuario'),
    path(r'^updateusuario/(?P<claveDocente>\d+)/',ModificarUsuario,name='ModificarUsuario'),
    path(r'^deleteusuario/(?P<claveDocente>\d+)/',EliminarUsuario,name='EliminarUsuario'),
    path('ConsultarUsuario',ConsultarUsuario,name='ConsultarUsuario'),

    #Calificaciones
    path('AgregarCalificaciones',AgregarCalificaciones,name='AgregarCalificaciones'),
    path('ModificarCalificaciones',Modificar_Calificaciones,name='Modificar_Calificaciones'),
    path('EliminarCalificaciones',Eliminar_Calificaciones,name='Eliminar_Calificaciones'),
    path(r'^updatecalificaciones/(?P<matricula>\d+)/',ModificarCalificaciones,name='ModificarCalificaciones'),
    path(r'^deletecalificaciones/(?P<matricula>\d+)/',EliminarCalificaciones,name='EliminarCalificaciones'),
    path('ConsultarCalificaciones',ConsultarCalificaciones,name='ConsultarCalificaciones'),

    #Materias
    path('AgregarMaterias',AgregarMaterias,name='AgregarMaterias'),
    path('ModificarMaterias',Modificar_Materias,name='Modificar_Materias'),
    path('EliminarMaterias',Eliminar_Materias,name='Eliminar_Materias'),
    path(r'^updatemateria/(?P<claveMateria>\d+)/',ModificarMaterias,name='ModificarMaterias'),
    path(r'^deletemateria/(?P<claveMateria>\d+)/',EliminarMaterias,name='EliminarMaterias'),
    path('ConsultarMaterias',ConsultarMaterias,name='ConsultarMaterias'),

    #Grupos
    path('AgregarGrupos',AgregarGrupos,name='AgregarGrupos'),
    path('ModificarGrupos',Modificar_Grupos,name='Modificar_Grupos'),
    path('EliminarGrupos',Eliminar_Grupos,name='Eliminar_Grupos'),
    path(r'^updategrupos/(?P<claveGrupo>\d+)/',ModificarGrupos,name='ModificarGrupos'),
    path(r'^deletegrupos/(?P<claveGrupo>\d+)/',EliminarGrupos,name='EliminarGrupos'),
    path('ConsultarGrupos',ConsultarGrupos,name='ConsultarGrupos'),
]