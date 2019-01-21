from PyQt4.QtCore import QStringList
from PyQt4.QtGui import QApplication, QFileDialog
from validate_email import validate_email

from controladores.ControladorBase import ControladorBase
from libs.Utiles import LeerIni, desencriptar, GrabarIni, encriptar
from vistas.Config import ConfigView
from libs import Ventanas

class ConfigController(ControladorBase):

    def __init__(self):
        super(ConfigController, self).__init__()
        self.view = ConfigView()
        self.view.initUi()
        self.conectarWidgets()
        self.CargaDatos()

    def conectarWidgets(self):
        self.view.btnCerrar.clicked.connect(self.Cerrar)
        self.view.btnGraba.clicked.connect(self.GrabaDatos)
        self.view.textCorreo.editingFinished.connect(lambda: self.ValidaEmail(self.view.textCorreo.text()))
        self.view.textCorreoErrores.editingFinished.connect(
            lambda: self.ValidaEmail(self.view.textCorreoErrores.text())
        )
        self.view.btnCertKEY.clicked.connect(
            lambda: self.CargaArchivo(self.view.textCertKEY, "KEY files (*.key)")
        )
        self.view.btnCertCRT.clicked.connect(
            lambda: self.CargaArchivo(self.view.textCertCRT, "CRT files (*.crt)")
        )

    def Cerrar(self):
        QApplication.exit(1)

    def CargaDatos(self):
        self.view.textInicioSistema.setText(LeerIni('iniciosistema'))
        self.view.textNombreSistema.setText(LeerIni('nombre_sistema'))
        self.view.cboBase.setText(LeerIni('base'))
        self.view.textUsuario.setText(LeerIni('usuario'))
        self.view.textHost.setText(LeerIni('host'))
        self.view.textPass.setText(desencriptar(LeerIni('password'),LeerIni('key')))
        self.view.textCUIT.setText(LeerIni('cuit', key='WSFEv1'))
        self.view.textCertCRT.setText(LeerIni('cert_prod', key='WSAA'))
        self.view.textCertKEY.setText(LeerIni('privatekey_prod', key='WSAA'))
        self.view.textCorreoErrores.setText(LeerIni('to_address', key='correo'))
        self.view.textUserSMTP.setText(LeerIni('user_smtp', key='correo'))
        self.view.textCorreo.setText(LeerIni('from_address', key='correo'))
        self.view.textPuertoSMTP.setText(LeerIni('puerto_smtp', key='correo'))
        self.view.textServidorSMTP.setText(LeerIni('server_smtp', key='correo'))
        if LeerIni('password_email', key='correo'):
            self.view.textPassSMTP.setText(desencriptar(LeerIni('password_email', key='correo'),
                                                        LeerIni('key_email', key='correo')))


    def GrabaDatos(self):
        GrabarIni(valor=self.view.textInicioSistema.text(), key='param', clave='iniciosistema')
        GrabarIni(valor=self.view.textNombreSistema.text(), key='param', clave='nombre_sistema')
        GrabarIni(valor=self.view.cboBase.text(), key='param', clave='base')
        GrabarIni(valor=self.view.textUsuario.text(), key='param', clave='usuario')
        GrabarIni(valor=self.view.textHost.text(), key='param', clave='host')
        clave, key = encriptar(str(self.view.textPass.text()).encode())
        GrabarIni(valor=clave, key='param', clave='password')
        GrabarIni(valor=key, key='param', clave='key')
        GrabarIni(valor=str(self.view.textCUIT.text()).replace('-',''), key='WSFEv1', clave='cuit')
        GrabarIni(valor=self.view.textCertKEY.text(), key='WSAA', clave='privatekey_prod')
        GrabarIni(valor=self.view.textCertCRT.text(), key='WSAA', clave='cert_prod')
        GrabarIni(valor=self.view.textCorreoErrores.text(), key='correo', clave='to_address')
        GrabarIni(valor=self.view.textUserSMTP.text(), key='correo', clave='from_address')
        GrabarIni(valor=self.view.textServidorSMTP.text(), key='correo', clave='server_smtp')

        clavesmtp, keysmtp = encriptar(str(self.view.textPassSMTP.text()).encode())
        GrabarIni(valor=clavesmtp, key='correo', clave='password_email')
        GrabarIni(valor=keysmtp, key='correo', clave='key_email')
        GrabarIni(valor=self.view.textPuertoSMTP.text(), key='correo', clave='puerto_smtp')
        GrabarIni(valor=self.view.textUserSMTP.text(), key='correo', clave='user_smtp')
        Ventanas.showAlert("Sistema", "Datos grabados correctamente")
        self.Cerrar()

    def ValidaEmail(self, correo=''):
        if not validate_email(correo):
            Ventanas.showAlert("Sistema", "El correo {} no es valido. Verifique!!!".format(self.view.textCorreo.text()))

    def CargaArchivo(self, control, filter=''):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setFilter(filter)
        filenames = QStringList()
        if dlg.exec_():
            filename = dlg.selectedFiles()[0]
            control.setText(filename)