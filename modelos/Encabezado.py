from datetime import datetime

from peewee import AutoField, DateField, CharField, DecimalField, IntegerField, TextField

from controladores.FE import FEv1
from modelos.ModeloBase import ModeloBase, BitBooleanField


class Encabezado(ModeloBase):

    nrocontrol = AutoField(db_column='ncontrol')
    fechacbte = DateField(default=datetime.today())
    tipocbte = CharField(max_length=3, default='')
    puntovta = CharField(max_length=4, default='')
    cbtenro = CharField(max_length=8, default='')
    tipodoc = CharField(max_length=2, default='')
    nrodoc = CharField(max_length=11, default='')
    imptotal = DecimalField(max_digits=12, decimal_places=4, default=0)
    imptotconc = DecimalField(max_digits=12, decimal_places=4, default=0)
    impneto = DecimalField(max_digits=12, decimal_places=4, default=0)
    impiva = DecimalField(max_digits=12, decimal_places=4, default=0)
    imptrib = DecimalField(max_digits=12, decimal_places=4, default=0)
    impopex = DecimalField(max_digits=12, decimal_places=4, default=0)
    cae = CharField(max_length=14, default='')
    vencecae = DateField()
    resultado = CharField(max_length=1, default='')
    motivoobs = CharField(max_length=250, default='')
    errcode = CharField(max_length=6, default='')
    errmsg = CharField(max_length=250, default='')
    transferido = BitBooleanField()
    empresa = IntegerField(default=1)
    concepto = CharField(max_length=1, default=FEv1.PRODUCTOS)
    errorprog = TextField()
    listo = BitBooleanField()
    tipows = CharField(max_length=2, default='WS')
    nrelacion = IntegerField(default=0)

    class Meta:
        table_name = 'encabeza'