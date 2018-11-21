from peewee import AutoField, CharField

from modelos.ModeloBase import ModeloBase


class Empresa(ModeloBase):

    codigo = AutoField()
    nombre = CharField(max_length=30, default='')
    basedatos = CharField(max_length=30, default='')
    cuit = CharField(max_length=13, default='')
    certificadocrt = CharField(max_length=150, default='')
    certificadokey = CharField(max_length=150, default='')

    class Meta:
        table_name = "empresas"