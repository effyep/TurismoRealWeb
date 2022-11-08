# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acompanantes(models.Model):
    idacompanantes = models.AutoField(db_column='idAcompanantes', primary_key=True)  # Field name made lowercase.
    nombres = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    apellidos = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    identificacion = models.CharField(unique=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    idreserva = models.ForeignKey('Reservas', models.DO_NOTHING, db_column='idReserva', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Acompanantes'


class Artefactos(models.Model):
    idartefactos = models.AutoField(db_column='idArtefactos', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tamano = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    valor = models.IntegerField(blank=True, null=True)
    idunidadmedida = models.ForeignKey('Unidadmedida', models.DO_NOTHING, db_column='idUnidadMedida', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Artefactos'


class Boleta(models.Model):
    idboleta = models.AutoField(db_column='idBoleta', primary_key=True)  # Field name made lowercase.
    mediodepago = models.CharField(db_column='medioDePago', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    banco = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    comprobante = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    efectivo = models.IntegerField(blank=True, null=True)
    vuelto = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    idreserva = models.ForeignKey('Reservas', models.DO_NOTHING, db_column='idReserva', blank=True, null=True)  # Field name made lowercase.
    iddetalleservicio = models.ForeignKey('Detalleservicio', models.DO_NOTHING, db_column='idDetalleServicio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Boleta'


class Comuna(models.Model):
    idcomuna = models.AutoField(db_column='idComuna', primary_key=True)  # Field name made lowercase.
    comuna = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    idregion = models.ForeignKey('Region', models.DO_NOTHING, db_column='idRegion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comuna'


class Departamentos(models.Model):
    iddepartamento = models.AutoField(db_column='idDepartamento', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    direccion = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    canthabitaciones = models.IntegerField(db_column='cantHabitaciones', blank=True, null=True)  # Field name made lowercase.
    cantbanos = models.IntegerField(db_column='cantBanos', blank=True, null=True)  # Field name made lowercase.
    precionoche = models.IntegerField(db_column='precioNoche', blank=True, null=True)  # Field name made lowercase.
    mantinicio = models.DateField(db_column='mantInicio', blank=True, null=True)  # Field name made lowercase.
    manttermino = models.DateField(db_column='mantTermino', blank=True, null=True)  # Field name made lowercase.
    idcomuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='idComuna', blank=True, null=True)  # Field name made lowercase.
    idestadodepto = models.ForeignKey('Estadodepto', models.DO_NOTHING, db_column='idEstadoDepto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departamentos'


class Detalleinconveniente(models.Model):
    iddetalleinconveniente = models.AutoField(db_column='idDetalleInconveniente', primary_key=True)  # Field name made lowercase.
    detalle = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mediodepago = models.CharField(db_column='medioDePago', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    banco = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    comprobante = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    efectivo = models.IntegerField(blank=True, null=True)
    vuelto = models.IntegerField(blank=True, null=True)
    idreserva = models.ForeignKey('Reservas', models.DO_NOTHING, db_column='idReserva', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DetalleInconveniente'


class Detalleservicio(models.Model):
    iddetalleservicio = models.AutoField(db_column='idDetalleServicio', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    montototal = models.IntegerField(db_column='montoTotal', blank=True, null=True)  # Field name made lowercase.
    idservicio = models.ForeignKey('Servicios', models.DO_NOTHING, db_column='idServicio', blank=True, null=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DetalleServicio'


class Estadodepto(models.Model):
    idestadodepto = models.AutoField(db_column='idEstadoDepto', primary_key=True)  # Field name made lowercase.
    estadodepto = models.CharField(db_column='estadoDepto', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EstadoDepto'


class Galeria(models.Model):
    idgaleria = models.AutoField(db_column='idGaleria', primary_key=True)  # Field name made lowercase.
    descripcionimagen = models.CharField(db_column='descripcionImagen', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    imagen = models.BinaryField(blank=True, null=True)
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='idDepartamento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Galeria'


class Gastos(models.Model):
    idgastos = models.AutoField(db_column='idGastos', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    fechagastos = models.DateField(db_column='fechaGastos', blank=True, null=True)  # Field name made lowercase.
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='idDepartamento', blank=True, null=True)  # Field name made lowercase.
    idtipogastos = models.ForeignKey('Tipogasto', models.DO_NOTHING, db_column='idTipoGastos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Gastos'


class Inventario(models.Model):
    idinventario = models.AutoField(db_column='idInventario', primary_key=True)  # Field name made lowercase.
    cantidad = models.IntegerField(blank=True, null=True)
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='idDepartamento', blank=True, null=True)  # Field name made lowercase.
    idartefactos = models.ForeignKey(Artefactos, models.DO_NOTHING, db_column='idArtefactos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inventario'


class Region(models.Model):
    idregion = models.AutoField(db_column='idRegion', primary_key=True)  # Field name made lowercase.
    region = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'Region'


class Reportes(models.Model):
    idreporte = models.AutoField(db_column='idReporte', primary_key=True)  # Field name made lowercase.
    total = models.IntegerField(blank=True, null=True)
    cantreservas = models.IntegerField(db_column='cantReservas', blank=True, null=True)  # Field name made lowercase.
    gastos = models.IntegerField(blank=True, null=True)
    fechadesde = models.DateField(db_column='fechaDesde', blank=True, null=True)  # Field name made lowercase.
    fechahasta = models.DateField(db_column='fechaHasta', blank=True, null=True)  # Field name made lowercase.
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='idDepartamento', blank=True, null=True)  # Field name made lowercase.
    idregion = models.ForeignKey(Region, models.DO_NOTHING, db_column='idRegion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reportes'


class Reservas(models.Model):
    idreserva = models.AutoField(db_column='idReserva', primary_key=True)  # Field name made lowercase.
    fechadesde = models.DateField(db_column='fechaDesde', blank=True, null=True)  # Field name made lowercase.
    fechahasta = models.DateField(db_column='fechaHasta', blank=True, null=True)  # Field name made lowercase.
    estadoreserva = models.CharField(db_column='estadoReserva', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    abono = models.IntegerField(blank=True, null=True)
    checkin = models.DateTimeField(db_column='checkIn', blank=True, null=True)  # Field name made lowercase.
    chekout = models.DateTimeField(db_column='chekOut', blank=True, null=True)  # Field name made lowercase.
    fechahorareserva = models.DateTimeField(db_column='fechaHoraReserva', blank=True, null=True)  # Field name made lowercase.
    precionochereserva = models.IntegerField(db_column='precioNocheReserva', blank=True, null=True)  # Field name made lowercase.
    saldo = models.IntegerField(blank=True, null=True)
    preciototalreserva = models.IntegerField(db_column='precioTotalReserva', blank=True, null=True)  # Field name made lowercase.
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='idDepartamento', blank=True, null=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reservas'


class Servicios(models.Model):
    idservicio = models.AutoField(db_column='idServicio', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    disponibilidad = models.CharField(max_length=13, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    idtiposervicio = models.ForeignKey('Tiposervicios', models.DO_NOTHING, db_column='idTipoServicio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Servicios'


class Tipogasto(models.Model):
    idtipogasto = models.AutoField(db_column='idTipoGasto', primary_key=True)  # Field name made lowercase.
    tipogasto = models.CharField(db_column='tipoGasto', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoGasto'


class Tiposervicios(models.Model):
    idtiposervicio = models.AutoField(db_column='idTipoServicio', primary_key=True)  # Field name made lowercase.
    tiposervicio = models.CharField(db_column='tipoServicio', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoServicios'


class Tipousuarios(models.Model):
    idtipousuario = models.AutoField(db_column='idTipoUsuario', primary_key=True)  # Field name made lowercase.
    tipousuario = models.CharField(db_column='tipoUsuario', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoUsuarios'


class Unidadmedida(models.Model):
    idunidadmedida = models.AutoField(db_column='idUnidadMedida', primary_key=True)  # Field name made lowercase.
    tipounidad = models.CharField(db_column='tipoUnidad', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadMedida'


class Usuarios(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    nombres = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    apellidos = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    usuario = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    correo = models.CharField(unique=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    contrasena = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS')
    identificacion = models.CharField(unique=True, max_length=9, db_collation='SQL_Latin1_General_CP1_CI_AS')
    celular = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    pais = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    codigoverificacion = models.CharField(db_column='codigoVerificacion', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    habilitada = models.CharField(max_length=13, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    espasaporte = models.CharField(db_column='esPasaporte', max_length=9, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    idtipousuario = models.ForeignKey(Tipousuarios, models.DO_NOTHING, db_column='idTipoUsuario', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usuarios'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
