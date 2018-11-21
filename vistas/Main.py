# coding=utf-8
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout

from libs.BarraProgreso import Avance
from libs.Botones import BotonCerrarFormulario, Boton
from libs.Etiquetas import EtiquetaTitulo, Etiqueta
from libs.Grillas import Grilla
from libs.Utiles import LeerIni
from vistas.VistaBase import VistaBase


class MainView(VistaBase):

    def initUi(self):
        self.setGeometry(150, 150, 650, 450)
        self.setWindowTitle('Factura Electronica - Servidor MySql {}'.format(LeerIni(clave='host')))
        self.layoutPpal = QVBoxLayout(self)
        self.lblTitulo = EtiquetaTitulo(texto="{}-{}-{}".format(
            LeerIni(clave="nombre_sistema"), LeerIni(clave='EMPRESA', key='FACTURA'),
                                        "Homologacion" if LeerIni("homo") == "S" else "Produccion"))
        self.layoutPpal.addWidget(self.lblTitulo)

        self.avance = Avance()
        self.layoutPpal.addWidget(self.avance)

        self.lblProcesamiento = Etiqueta()
        self.layoutPpal.addWidget(self.lblProcesamiento)

        self.gridFacturas = Grilla()
        cabeceras = [
            'Pto Vta', 'Comprobante', 'CAE', 'Vence Cae', 'Errores'
        ]
        self.gridFacturas.ArmaCabeceras(cabeceras=cabeceras)
        self.layoutPpal.addWidget(self.gridFacturas)

        self.btnCerrar = BotonCerrarFormulario()
        self.btnIniciar = Boton(texto='Iniciar', imagen='imagenes/Accept.png')
        layoutBotones = QHBoxLayout()
        layoutBotones.addWidget(self.btnIniciar)
        layoutBotones.addWidget(self.btnCerrar)

        self.layoutPpal.addLayout(layoutBotones)