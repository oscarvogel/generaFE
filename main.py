# coding=utf-8
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Punto de Inicio del sistema
import os

from modelos.CAEA import CAEA
from modelos.CbteRelacionado import CbteRel
from modelos.Empresas import Empresa
from modelos.IVA import IVA
from modelos.Tributo import Tributo

__author__ = "Jose Oscar Vogel <oscarvogel@gmail.com>"
__copyright__ = "Copyright (C) 2018 Jose Oscar Vogel"
__license__ = "GPL 3.0"
__version__ = "0.5"

import logging
import sys
from datetime import datetime

from os.path import join

from PyQt4.QtGui import QApplication

from controladores.FE import FEv1
from controladores.Main import MainController
from libs.Utiles import LeerIni, FechaMysql, envia_correo, DeCodifica, encriptar, GrabarIni
from modelos.Encabezado import Encabezado


def inicio():
    if LeerIni("iniciosistema") == "":
        #GrabarIni(clave='password', key='param', valor=claveencriptada)
        GrabarIni(valor=os.getcwd() + "\\", key="param", clave="iniciosistema")
    logging.basicConfig(filename=join(LeerIni("iniciosistema"), 'errors.log'), level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    if LeerIni(clave='homo') == 'S':
        print("Sistema en modo homologacion")
    else:
        print("Sistema en modo produccion")
    # Instancia para iniciar una aplicación
    args = []
    #args = ['', '-style', 'Cleanlooks']
    app = QApplication(args)
    ex = MainController()
    ex.run()
    sys.exit(app.exec_())

if __name__ == "__main__":

    if "--caea" in sys.argv:
        periodo = FechaMysql()[:6]

        if FechaMysql()[-2:] > '15':
            orden = '2'
        else:
            orden = '1'

        wsfe = FEv1()
        caea = wsfe.SolicitarCAEA(periodo, orden)
        print("CAEA {} periodo {} orden {} FchVigDesde {} FchVigHasta {} FchTopeInf {} FchProceso {}".
              format(caea, wsfe.Periodo, wsfe.Orden, wsfe.FchVigDesde, wsfe.FchVigHasta,
                     wsfe.FchTopeInf, wsfe.FchProceso))
    elif "--informacaea" in sys.argv:
        punto_vta = sys.argv[sys.argv.index("--informacaea")+1]
        caea = sys.argv[sys.argv.index("--informacaea") + 2]

        data = Encabezado.select().where(Encabezado.resultado == 'A',
                                         Encabezado.tipows == 'A',
                                         Encabezado.puntovta == punto_vta,
                                         Encabezado.cae == caea)
        if data.count() == 0:
            wsfe = FEv1()
            wsfe.InformarCAEASinMovimiento(punto_vta, caea)
        else:
            controlador = MainController()
            for d in data:
                print("Procesando factura {}-{}".format(d.puntovta, d.cbtenro))
                ok = controlador.CreaFE(d, caea=True)
                if ok:
                    d.cae = controlador.cae
                    d.resultado = controlador.resultado
                    d.cbtenro = str(controlador.comprobante).zfill(8)
                    d.vencecae = datetime.strptime(controlador.vencecae, '%Y%m%d')
                else:
                    d.resultado = controlador.resultado
                    d.errmsg = controlador.errmsg
                    d.motivoobs = controlador.motivoobs
                    d.vencecae = datetime.today()
                    envia_correo(to_address='oscar@ferreteriaavenida.com.ar',
                                 from_address='info@ferreteriaavenida.com.ar',
                                 subject='Error al generar FE',
                                 message="Error: {} {}".format(DeCodifica(controlador.errmsg),
                                                               DeCodifica(controlador.motivoobs)),
                                 password_email='Fasa0298')
                d.save()

    elif "--clavemysql" in sys.argv:
        clave = raw_input("Ingresa la clave: ")
        claveencriptada, keyencriptado = encriptar(password=clave)
        GrabarIni(clave='password',key='param', valor=claveencriptada)
        GrabarIni(clave='key', key='param', valor=keyencriptado)

    elif "--creatablas" in sys.argv:
        encabeza = Encabezado()
        encabeza.create_table(True)
        iva = IVA()
        iva.create_table(True)
        tributo = Tributo()
        tributo.create_table(True)
        cbterel = CbteRel()
        cbterel.create_table(True)
        empresa = Empresa()
        empresa.create_table(True)
        caea = CAEA()
        caea.create_table(True)

    elif "--help" in sys.argv or "-h" in sys.argv:
        print("--clavemysql graba la contraseña de mysql")
        print("--creatablas crea tablas segun lo configurado en el sistema.ini")
    else:
        inicio()
