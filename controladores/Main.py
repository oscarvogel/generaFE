# coding=utf-8
import calendar
import traceback
from datetime import datetime

from PyQt4.QtGui import QApplication
from peewee import fn

from controladores.ControladorBase import ControladorBase
from controladores.FE import FEv1
from libs.Utiles import LeerIni, FechaMysql, envia_correo, DeCodifica
from modelos.CAEA import CAEA
from modelos.CbteRelacionado import CbteRel
from modelos.Encabezado import Encabezado
from modelos.IVA import IVA
from modelos.ModeloBase import ModeloBase
from modelos.Tributo import Tributo
from vistas.Main import MainView


class MainController(ControladorBase):

    lProcesa = True
    cae = ''
    vencecae = ''
    errmsg = ''
    resultado = ''
    motivoobs = ''
    comprobante = ''
    xml_response = ''
    xml_request = ''
    grabaxml = False

    def __init__(self):
        super(MainController, self).__init__()
        self.view = MainView()
        self.view.initUi()
        self.conectarWidgets()
        self.model = ModeloBase()
        self.model.getDb()

    def conectarWidgets(self):
        self.view.btnCerrar.clicked.connect(self.Cerrar)
        self.view.btnIniciar.clicked.connect(self.GeneraFE)

    def Cerrar(self):
        self.lProcesa = False
        QApplication.exit(1)

    def GeneraFE(self):
        self.view.btnIniciar.setEnabled(False)
        while self.lProcesa:
            QApplication.processEvents()
            #self.ObtieneCAEA() #obtiene CAE Anticipado 5 dias antes del inicio de la quincena
            self.GeneraCAE() #si tenemos internet obtenemos CAE
            #self.GeneraCAEA() #en caso de que no haya internet usamos el CAEA

    def CreaFE(self, d, caea = None):
        ok = True
        cbterel = None
        wsfev1 = FEv1()
        ta = wsfev1.Autenticar()
        #Setear tocken y sign de autorizacion(ticket de accesso, pasos previos)
        wsfev1.SetTicketAcceso(ta)
        #Conectar al Servicio Web de Facturacion
        #Produccion usar: *-- ok = WSFE.Conectar("", "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL") & & Producción
        if LeerIni(clave='homo') == 'S':
            wsfev1.Cuit = '20233472035'  # CUIT del programador para pruebas
            ok = wsfev1.Conectar("") #Homologacion
        else:
            wsfev1.Cuit = LeerIni(clave='cuit', key='WSFEv1')  # CUIT del emisor (debe estar registrado en la AFIP)
            ok = wsfev1.Conectar("", "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL")

        concepto = d.concepto
        tipo_doc = d.tipodoc
        punto_vta = d.puntovta
        tipo_cbte = d.tipocbte
        nro_doc = d.nrodoc
        cbt_desde = int(wsfev1.UltimoComprobante(tipo=tipo_cbte, ptovta=punto_vta)) + 1
        cbt_hasta = cbt_desde
        imp_total = str(round(d.imptotal, 2))
        imp_tot_conc = "0.00"
        imp_neto = str(round(d.impneto, 2))
        imp_iva = str(round(d.impiva, 2))
        imp_trib = str(round(d.imptrib,2))
        impto_liq_rni = "0.00"
        imp_op_ex = str(round(d.impopex, 2))
        fecha_cbte = FechaMysql(d.fechacbte)
        #Fechas del periodo del servicio facturado(solo siconcepto > 1)
        if concepto in [wsfev1.SERVICIOS, wsfev1.PRODUCTOYSERVICIOS]:
            fecha_serv_desde = fecha_cbte
            fecha_serv_hasta = fecha_cbte
            fecha_venc_pago = fecha_cbte
        else:
            fecha_serv_desde = ""
            fecha_serv_hasta = ""
            fecha_venc_pago = ""

        moneda_id = "PES"
        moneda_ctz = "1.000"

        #Llamo al WebService de Autorizacion para obtener el CAE
        wsfev1.CrearFactura(concepto, tipo_doc, nro_doc, tipo_cbte, punto_vta,
                cbt_desde, cbt_hasta, imp_total, imp_tot_conc, imp_neto,
                imp_iva, imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago,
                fecha_serv_desde, fecha_serv_hasta,
                moneda_id, moneda_ctz)

        #tributo = Tributo.select().where(Tributo.nrocontrol == d.nrocontrol)
        tributo = Tributo.select().where(Tributo.nrelacion == d.nrelacion)
        for t in tributo:
            idimp = t.tributoid
            detalle = t.descripcion
            base_imp = round(t.baseimp, 2)
            alicuota = round(t.alic, 2)
            importe = str(round(t.importe, 2))
            wsfev1.AgregarTributo(tributo_id=idimp, desc=detalle, base_imp=base_imp,
                                  alic=alicuota, importe=importe)

        #iva = IVA.select().where(IVA.nrocontrol == d.nrocontrol)
        iva = IVA.select().where(IVA.nrelacion == d.nrelacion)
        for i in iva:
            id = i.ivaid
            base_imp = round(i.baseimp, 2)
            iva = round(i.importe, 2)
            wsfev1.AgregarIva(id, base_imp, iva)

        #cbterel = CbteRel.select().where(CbteRel.nrocontrol == d.nrocontrol)
        cbterel = CbteRel.select().where(CbteRel.nrelacion == d.nrelacion)
        for c in cbterel:
            tipo = c.tipocbte
            pto_vta = c.ptovta
            nro = c.nrocbte
            wsfev1.AgregarCmpAsoc(tipo, pto_vta, nro)

        if caea:
            wsfev1.EstablecerCampoFactura('caea', d.cae)
            cae = wsfev1.CAEARegInformativo()
            #logging.warning(wsfev1.xml_request, wsfev1.xml_response)
            if self.grabaxml:
                f = open("xmlrequest.xml", "wb")
                f.write(wsfev1.xml_request)
                f.close()

                f = open("xmlresponse.xml", "wb")
                f.write(wsfev1.xml_response)
                f.close()

            self.xml_response = wsfev1.xml_response
            self.xml_request = wsfev1.xml_request
        else:
            #SolicitoCAE:
            cae = wsfev1.CAESolicitar()

        self.resultado = wsfev1.Resultado
        if wsfev1.ErrMsg:
            #Ventanas.showAlert("Sistema", "ERROR {}".format(wsfev1.ErrMsg))
            self.errmsg = wsfev1.ErrMsg
            self.xml_response = wsfev1.xml_response
            self.xml_request = wsfev1.xml_request
            ok = False
            item = [
                punto_vta, '', '', '', wsfev1.ErrMsg
            ]
        else:
            if wsfev1.Resultado == 'R':
                #Ventanas.showAlert("Sistema", "Motivo de rechazo {}".format(wsfev1.Obs))
                self.xml_response = wsfev1.xml_response
                self.xml_request = wsfev1.xml_request
                self.motivoobs = wsfev1.Obs
                item = [
                    punto_vta, '', '', '', wsfev1.Obs
                ]
                ok = False
            else:
                self.cae = cae
                self.vencecae = wsfev1.Vencimiento
                self.comprobante = cbt_desde
                item = [
                    punto_vta, str(cbt_desde).zfill(8), cae, wsfev1.Vencimiento, ''
                ]
                print("Vencimiento cae {}".format(wsfev1.Vencimiento))

        if self.view.gridFacturas.rowCount() > 10:
            self.view.gridFacturas.removeRow(0)

        self.view.gridFacturas.AgregaItem(items=item)
        return ok

    def ObtieneCAEA(self):
        dia = datetime.now().day
        periodo = FechaMysql()[:6]
        obtener = True
        if dia < 15:
            orden = '1'
            if dia + 5 == 15:
                obtener = True
        else:
            orden = '2'
            if dia + 5 == calendar.monthrange(int(periodo[:4]), int(periodo[4:6]))[1]:
                obtener = True

        if obtener:
            try:
                data = CAEA.select().where(CAEA.periodo == periodo,
                                           CAEA.orden == orden).get()
            except CAEA.DoesNotExist:
                print("caea no existe")
                wsfe = FEv1()
                wsfe.SolicitarCAEA(periodo, orden)
                caea = CAEA()
                caea.CAEA = wsfe.CAEA
                caea.periodo = wsfe.Periodo
                caea.orden = wsfe.Orden
                caea.fchvigdesde = wsfe.FchVigDesde
                caea.fchvighasta = wsfe.FchVigHasta
                caea.fchproceso = wsfe.FchProceso
                caea.fchtopeinf = wsfe.FchTopeInf
                caea.obs = wsfe.Obs
                caea.empresa = 1 #ferreteria por ahora tengo que ver como hacer para las otras empresas
                caea.save()

    def GeneraCAE(self):
        data = Encabezado.select().where(Encabezado.resultado == '',
                                         Encabezado.listo == b'\01',
                                         Encabezado.tipows == 'WS')
        total = data.count() or 1
        i = 1.
        for d in data:
            try:
                self.view.lblProcesamiento.setText("Procesando comprobante {} de {}".format(i, total))
                self.view.avance.actualizar(i / total * 100)
                ok = self.CreaFE(d)
                if ok:
                    d.cae = self.cae
                    d.resultado = self.resultado
                    d.cbtenro = str(self.comprobante).zfill(8)
                    d.vencecae = datetime.strptime(self.vencecae, '%Y%m%d')
                else:
                    d.resultado = self.resultado
                    d.errmsg = self.errmsg
                    d.motivoobs = self.motivoobs
                    d.vencecae = datetime.today()
                    envia_correo(to_address='oscar@ferreteriaavenida.com.ar',
                                 from_address='info@ferreteriaavenida.com.ar',
                                 subject='Error al generar FE',
                                 message="Error: {} {}".format(DeCodifica(self.errmsg),
                                                               DeCodifica(self.motivoobs)),
                                 password_email='Fasa0298')
                d.save()
                i += 1
            except Exception as e:
                d.resultado = 'E'
                d.errmsg = "Error: {}".format(e)
                d.vencecae = datetime.today()
                d.errorprog = traceback.format_exc()
                d.save()
                print "Error: {}".format(e)
                envia_correo(to_address='oscar@ferreteriaavenida.com.ar',
                             from_address='info@ferreteriaavenida.com.ar',
                             subject='Error al generar FE',
                             message="Error: {} {}".format(e, traceback.format_exc()),
                             password_email='Fasa0298')

        self.view.lblProcesamiento.setText("Sin comprobantes para procesar")
        self.view.avance.actualizar(100)

    #genera facturas con CAEA para el caso de que no haya internet
    def GeneraCAEA(self):
        data = Encabezado.select().where(Encabezado.resultado == '',
                                         Encabezado.listo == b'\01',
                                         Encabezado.tipows == 'A')
        total = data.count() or 1
        i = 1.
        for d in data:
            self.view.lblProcesamiento.setText("Procesando comprobante {} de {}".format(i, total))
            self.view.avance.actualizar(i / total * 100)
            dia = datetime.now().day
            periodo = FechaMysql()[:6]
            if dia < 15:
                orden = '1'
            else:
                orden = '2'

            try:
                encabeza = Encabezado.select(fn.MAX(Encabezado.cbtenro)).\
                    where(Encabezado.puntovta == d.puntovta).scalar()
                datacaea = CAEA.select().where(CAEA.periodo == periodo,
                                           CAEA.orden == orden).get()
                d.cbtenro = str(int(encabeza if encabeza else '0') + 1).zfill(8)
                d.cae = datacaea.CAEA
                d.vencecae = datacaea.fchtopeinf
                d.resultado = 'A'
                d.save()
            except CAEA.DoesNotExist:
                d.resultado = 'E'
                d.errmsg = 'No existe CAEA para el periodo y orden'
                d.vencecae = datetime.today()
                d.save()
                envia_correo(to_address='oscar@ferreteriaavenida.com.ar',
                             from_address='info@ferreteriaavenida.com.ar',
                             subject='Error al generar FE con CAEA',
                             message="Error: {}".format(d.errmsg),
                             password_email='Fasa0298')