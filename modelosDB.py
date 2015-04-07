# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Cuentas(models.Model):
    id_user = models.IntegerField(primary_key=True)
    nombreusuario = models.CharField(max_length=80)
    contrase_a = models.CharField(db_column='contrase\xf1a', max_length=80)  # Field renamed to remove unsuitable characters.
    e_mail = models.CharField(max_length=80)
    fechanacimiento = models.DateField()
    nombreyapellido = models.CharField(max_length=160)
    deleted = models.BooleanField()
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


class Login(models.Model):
    id_user = models.ForeignKey(Cuentas, db_column='id_user', primary_key=True)
    email = models.CharField(max_length=80)
    contrase_a = models.CharField(db_column='contrase\xf1a', max_length=80)  # Field renamed to remove unsuitable characters.

    class Meta:
        db_table = 'login'


class Perfiles(models.Model):
    id_perfil = models.IntegerField(primary_key=True)
    id_user = models.ForeignKey(Cuentas, db_column='id_user')
    perfil = models.CharField(max_length=15)

    class Meta:
        db_table = 'perfiles'
