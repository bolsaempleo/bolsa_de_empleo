from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.


class CodigoDeCambio(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=60, null=True, db_column='codigo')
    login_id = models.ForeignKey('Login', db_column='login_id')

    class Meta:

        db_table = 'codigo_de_cambio'

class Login(User):
    id_user = models.ForeignKey('Cuentas', db_column='id_user', null=True, blank=True)
    contrase_a = models.CharField(db_column='contrasena', max_length=80)  # Field renamed to remove unsuitable characters.

    objects = UserManager()

    class Meta:

        db_table = 'login'

class Cuentas(models.Model):
    id_user = models.AutoField(primary_key=True)
    nombreusuario = models.CharField(max_length=80)  # codigo
    contrase_a = models.CharField(db_column='contrasena', max_length=80)  # Field renamed to remove unsuitable characters.
    e_mail = models.CharField(max_length=80)
    fechanacimiento = models.DateField()
    nombreyapellido = models.CharField(max_length=160)
    deleted = models.BooleanField(default=False)
    log_count = models.IntegerField()
    estado = models.CharField(max_length=15)

    class Meta:
        db_table = 'cuentas'

class Funcionario(models.Model):
    id_user = models.ForeignKey(Cuentas, db_column='id_user', primary_key=True)
    id_empresa = models.ForeignKey('Infoempresa', db_column='id_empresa')
    cargo = models.CharField(max_length=80)

    class Meta:
        db_table = 'funcionario'


class Infoempresa(models.Model):
    id_user = models.ForeignKey(Cuentas, db_column='id_user', primary_key=True)
    numeroidentificacion = models.CharField(max_length=80, null=True, blank=True)
    razonsocial = models.CharField(max_length=160, null=True, blank=True)
    nrotrabajadores = models.IntegerField(null=True, blank=True)
    representantelegal = models.CharField(max_length=160, null=True, blank=True)
    e_mailrepresentlegal = models.CharField(max_length=80, null=True, blank=True)
    tipoempresa = models.CharField(max_length=80, null=True, blank=True)
    naturaleza = models.CharField(max_length=80, null=True, blank=True)
    jerarquia = models.CharField(max_length=80, null=True, blank=True)
    actividadeconomica = models.CharField(max_length=80, null=True, blank=True)
    pais = models.CharField(max_length=80, null=True, blank=True)
    departamento = models.CharField(max_length=80, null=True, blank=True)
    municipio = models.CharField(max_length=80, null=True, blank=True)
    barrio = models.CharField(max_length=80, null=True, blank=True)
    direccion = models.CharField(max_length=80, null=True, blank=True)
    indicativotelefonico = models.CharField(max_length=5, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    extension = models.CharField(max_length=5, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    paginaweb = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        db_table = 'infoempresa'


class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Cuentas, db_column='id_user')
    perfil = models.CharField(max_length=15, null=True)

    class Meta:
        db_table = 'perfiles'
