from django.db import models

class Region(models.Model):
    idregion = models.AutoField(db_column='idRegion', primary_key=True)  # Field name made lowercase.
    region = models.CharField(unique=True, max_length=50, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'Region'

class Comuna(models.Model):
    idcomuna = models.AutoField(db_column='idComuna', primary_key=True)  # Field name made lowercase.
    comuna = models.CharField(unique=True, max_length=50, db_collation='Modern_Spanish_CI_AS')
    idregion = models.ForeignKey('Region', models.DO_NOTHING, db_column='idRegion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comuna'

class Estadodepto(models.Model):
    idestadodepto = models.AutoField(db_column='idEstadoDepto', primary_key=True)  # Field name made lowercase.
    estadodepto = models.CharField(db_column='estadoDepto', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EstadoDepto'
        
class Departamentos(models.Model):
    iddepartamento = models.AutoField(db_column='idDepartamento', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    direccion = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    canthabitaciones = models.IntegerField(db_column='cantHabitaciones', blank=True, null=True)  # Field name made lowercase.
    cantbanos = models.IntegerField(db_column='cantBanos', blank=True, null=True)  # Field name made lowercase.
    precionoche = models.IntegerField(db_column='precioNoche', blank=True, null=True)  # Field name made lowercase.
    fechaestadodepto = models.DateField(db_column='fechaEstadoDepto', blank=True, null=True)  # Field name made lowercase.
    idcomuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='idComuna', blank=True, null=True)  # Field name made lowercase.
    idestadodepto = models.ForeignKey('Estadodepto', models.DO_NOTHING, db_column='idEstadoDepto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamentos'
# Create your models here.
