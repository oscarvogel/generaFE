from peewee import AutoField, CharField

from modelos.ModeloBase import ModeloBase


CUIT = {
    1:'30522884363',
    2:'30710940262',
    3:'30708792892'
}

class Empresa(ModeloBase):

    codigo = AutoField()
    nombre = CharField(max_length=30, default='')
    basedatos = CharField(max_length=30, default='')