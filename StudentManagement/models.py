from django.db import models

#Alumnos
class alumnos(models.Model):
    matricula = models.CharField(db_column='matricula', primary_key=True, max_length=6)  # Field name made lowercase.
    password = models.CharField(db_column='password', max_length=15, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='nombre', max_length=80, blank=True, null=True)  # Field name made lowercase.
    apellidoP = models.CharField(db_column='apellidoP', max_length=80, blank=True, null=True)  # Field name made lowercase.
    apellidoM = models.CharField(db_column='apellidoM', max_length=80, blank=True, null=True)  # Field name made lowercase.
    nombreP = models.CharField(db_column='nombreP', max_length=80, blank=True, null=True)  # Field name made lowercase.
    grado = models.CharField(db_column='grado',max_length=80, blank=True, null=True)  # Field name made lowercase.
    grupo = models.CharField(db_column='grupo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'alumnos'
        #fields = ('matricula', 'password', 'nombre', 'apellidoP', 'apellidoM', 'grado', 'grupo', 'nombreP', 'apellidoPP', 'apellidoMP') 
    def __str__(self):
        return self.matricula
    objects = models.Manager()

#Docentes
class docentes(models.Model):
    claveDocente = models.CharField(db_column='claveDocente', max_length=5, primary_key=True, blank=True)  # Field name made lowercase.
    password = models.CharField(db_column='password', max_length=15, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='nombre', max_length=80, blank=True, null=True)  # Field name made lowercase.
    apellidoP = models.CharField(db_column='apellidoP', max_length=80, blank=True, null=True)  # Field name made lowercase.
    apellidoM = models.CharField(db_column='apellidoM', max_length=80, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='email', max_length=80, blank=True, null=True)  # Field name made lowercase.
    curp = models.CharField(db_column='curp', max_length=80, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'docentes'
    def __str__(self):
        return self.claveDocente
    objects = models.Manager()

#Materias
class materias(models.Model):
    claveMateria = models.CharField(db_column='claveMateria', max_length=10,primary_key=True, blank=True)  # Field name made lowercase. = models.CharField(db_column='claveMateria', max_length=80, blank=True, null=True)  # Field name made lowercase.
    nombreMateria = models.CharField(db_column='nombreMateria', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materias'
    def __str__(self):
        return self.claveMateria
        return self.nombreMateria
    objects = models.Manager()

#Grupos
class grupos(models.Model):
    claveGrupo = models.CharField(db_column='claveGrupo', max_length=5, blank=True, primary_key=True)  # Field name made lowercase.
    #claveDocente = models.CharField(db_column='claveDocente', max_length=5, blank=True, null=True)  # Field name made lowercase..
    #claveMateria = models.CharField(db_column='claveMateria', max_length=5, blank=True, null=True)  # Field name made lowercase. 
    grado = models.CharField(db_column='grado',max_length=1, blank=True, null=True)  # Field name made lowercase.
    grupo = models.CharField(db_column='grupo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'groups'
    def __str__(self):
        return self.claveGrupo
    objects = models.Manager()

#Calificaciones
class calificacion(models.Model):
    incremento = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(alumnos,  db_column='matricula', on_delete = models.CASCADE)  # Field name made lowercase.
    claveMateria = models.ForeignKey(materias,  db_column='claveMateria', on_delete = models.CASCADE)  # Field name made lowercase.
    calif = models.CharField(db_column='calif', max_length=3, blank=True, null=True)  # Field name made lowercase.
    estrategia = models.CharField(db_column='estrategia', max_length=300, blank=True, null=True)  # Field name made lowercase.
    
    class Meta: 
        managed = False
        db_table = 'calificacion'
        #unique_together = ('matricula', 'claveMateria') 
     
    def __str__(self):
        return self.incremento
    objects = models.Manager()
