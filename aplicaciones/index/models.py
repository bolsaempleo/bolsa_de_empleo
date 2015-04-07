from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
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
    numeroidentificacion = models.CharField(max_length=80)
    razonsocial = models.CharField(max_length=160)
    nrotrabajadores = models.IntegerField()
    representantelegal = models.CharField(max_length=160)
    e_mailrepresentlegal = models.CharField(max_length=80)
    tipoempresa = models.CharField(max_length=80)
    naturaleza = models.CharField(max_length=80)
    jerarquia = models.CharField(max_length=80)
    actividadeconomica = models.CharField(max_length=80)
    pais = models.CharField(max_length=80)
    departamento = models.CharField(max_length=80)
    municipio = models.CharField(max_length=80)
    barrio = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80)
    indicativotelefonico = models.CharField(max_length=5)
    telefono = models.CharField(max_length=10)
    extension = models.CharField(max_length=5)
    celular = models.CharField(max_length=15)
    paginaweb = models.CharField(max_length=80)

    class Meta:
        db_table = 'infoempresa'


class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Cuentas, db_column='id_user')
    perfil = models.CharField(max_length=15)

    class Meta:
        db_table = 'perfiles'
