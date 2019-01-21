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

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLineEdit

from libs.Botones import Boton, BotonCerrarFormulario
from libs.CombosBox import ComboBase
from libs.EntradaTexto import EntradaTexto
from libs.Etiquetas import EtiquetaTitulo, Etiqueta
from vistas.VistaBase import VistaBase



class ConfigView(VistaBase):

    def initUi(self):
        self.setWindowTitle("Configuracion del sistema")
        layoutPpal = QVBoxLayout(self)
        lblTitulo = EtiquetaTitulo(texto=self.windowTitle())
        layoutPpal.addWidget(lblTitulo)

        layoutLinea1 = QHBoxLayout()
        lblInicioSistema = Etiqueta(texto='Inicio Sistema')
        self.textInicioSistema = EntradaTexto()
        layoutLinea1.addWidget(lblInicioSistema)
        layoutLinea1.addWidget(self.textInicioSistema)

        lblNombreSistema = Etiqueta(texto='Nombre Sistema')
        self.textNombreSistema = EntradaTexto()
        layoutLinea1.addWidget(lblNombreSistema)
        layoutLinea1.addWidget(self.textNombreSistema)
        layoutPpal.addLayout(layoutLinea1)

        layoutLinea2 = QHBoxLayout()
        lblBase = Etiqueta(texto='Tipo BD')
        self.cboBase = ComboBase()
        layoutLinea2.addWidget(lblBase)
        layoutLinea2.addWidget(self.cboBase)
        layoutPpal.addLayout(layoutLinea2)

        lblUsuario = Etiqueta(texto='Usuario')
        self.textUsuario = EntradaTexto()
        layoutLinea2.addWidget(lblUsuario)
        layoutLinea2.addWidget(self.textUsuario)

        lblHost = Etiqueta(texto='Host')
        self.textHost = EntradaTexto()
        layoutLinea2.addWidget(lblHost)
        layoutLinea2.addWidget(self.textHost)

        layoutLinea3 = QHBoxLayout()
        lblPass = Etiqueta(texto='Password')
        self.textPass = EntradaTexto()
        self.textPass.setEchoMode(QLineEdit.Password)
        layoutLinea3.addWidget(lblPass)
        layoutLinea3.addWidget(self.textPass)
        lblCUIT = Etiqueta(texto='CUIT/CUIL')
        self.textCUIT = EntradaTexto()
        layoutLinea3.addWidget(lblCUIT)
        layoutLinea3.addWidget(self.textCUIT)
        layoutPpal.addLayout(layoutLinea3)

        layoutLinea4 = QHBoxLayout()
        lblCertCRT = Etiqueta(texto="Llave Publica")
        self.textCertCRT = EntradaTexto()
        self.btnCertCRT = Boton(imagen='imagenes/buscar.png', texto='...', autodefault=False)
        layoutLinea4.addWidget(lblCertCRT)
        layoutLinea4.addWidget(self.textCertCRT)
        layoutLinea4.addWidget(self.btnCertCRT)
        lblCertKEY = Etiqueta(texto="Llave Privada")
        self.textCertKEY = EntradaTexto()
        self.btnCertKEY = Boton(imagen='imagenes/buscar.png', texto='...', autodefault=False)
        layoutLinea4.addWidget(lblCertKEY)
        layoutLinea4.addWidget(self.textCertKEY)
        layoutLinea4.addWidget(self.btnCertKEY)
        layoutPpal.addLayout(layoutLinea4)

        lblConfigCorreo = EtiquetaTitulo(texto="Configuracion de correo")
        layoutPpal.addWidget(lblConfigCorreo)

        layoutLinea5 = QHBoxLayout()
        lblCorreo = Etiqueta(texto="Quien envia el Correo")
        self.textCorreo = EntradaTexto(placeholderText="Quien envia el correo")
        layoutLinea5.addWidget(lblCorreo)
        layoutLinea5.addWidget(self.textCorreo)
        layoutPpal.addLayout(layoutLinea5)

        layoutLinea6 = QHBoxLayout()
        lblServidorSMTP = Etiqueta(texto="Servidor SMTP")
        self.textServidorSMTP = EntradaTexto(placeholderText="Servidor SMTP")
        layoutLinea6.addWidget(lblServidorSMTP)
        layoutLinea6.addWidget(self.textServidorSMTP)
        lblPuertoSMTP = Etiqueta(texto="Puerto SMTP")
        self.textPuertoSMTP = EntradaTexto(placeholderText="Puerto")
        layoutLinea6.addWidget(lblPuertoSMTP)
        layoutLinea6.addWidget(self.textPuertoSMTP)
        layoutPpal.addLayout(layoutLinea6)

        layoutLinea7 = QHBoxLayout()
        lblUsuarioCorreo = Etiqueta(texto="Usuario SMTP")
        self.textUserSMTP = EntradaTexto(placeholderText="Usuario SMTP")
        layoutLinea7.addWidget(lblUsuarioCorreo)
        layoutLinea7.addWidget(self.textUserSMTP)
        layoutPpal.addLayout(layoutLinea7)

        layoutLinea8 = QHBoxLayout()
        lblPassCorreo = Etiqueta(texto=u"Contraseña server SMPT")
        self.textPassSMTP = EntradaTexto(placeholderText="Password SMTP")
        self.textPassSMTP.setEchoMode(QLineEdit.Password)
        layoutLinea8.addWidget(lblPassCorreo)
        layoutLinea8.addWidget(self.textPassSMTP)
        layoutPpal.addLayout(layoutLinea8)

        layoutLinea9 = QHBoxLayout()
        lblCorreoErrores = Etiqueta(texto="Correo para errores")
        self.textCorreoErrores = EntradaTexto(placeholderText="Correo al que se envian los errores",
                                              tooltip="Correo al que se envian los errores que se producen")
        layoutLinea9.addWidget(lblCorreoErrores)
        layoutLinea9.addWidget(self.textCorreoErrores)
        layoutPpal.addLayout(layoutLinea9)

        layoutBotones = QHBoxLayout()
        self.btnGraba = Boton(imagen='imagenes/guardar.png', texto='Guardar')
        self.btnCerrar = BotonCerrarFormulario()
        layoutBotones.addWidget(self.btnGraba)
        layoutBotones.addWidget(self.btnCerrar)
        layoutPpal.addLayout(layoutBotones)