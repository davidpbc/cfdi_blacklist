import os
import base64
from datetime import datetime, timedelta
# UI Imports
from ui.main_ui import Ui_MainWindow as mainWindow
from ui.empresas_ui import Ui_mainWindow as empresaMW
from ui.empresa_fiel_ui import Ui_MainWindow as empresa_fielMW
from ui.request_packages_ui import Ui_MainWindow as req_packMW
from ui.add_empresa_ui import Ui_Dialog
from ui.add_fiel_ui import Ui_Dialog as fielDialog
from ui.add_request_ui import Ui_Dialog as requestDialog
from PyQt5.QtCore import QDate, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QTableWidgetItem,
    QInputDialog,
    QFileDialog,
)
# DB Imports
from models.base import Session, engine
from models.empresa import Empresa
from models.fiel import Fiel
from models.request import Request
from models.package import Package
from models.blacklist import Blacklist
# API SAT Imports
from download.certificate import Certificates
from download.authenticate import Authenticate
from download.cfdi_request import RequestDownload
from download.request_check import RequestCheck
from download.download import DownloadCFDi
# Local Imports
from update_blacklist import process_blacklist_update
from cfdi_xml import CfdiXml
from crud import recreate_database

s = Session()

ESTADOS_SAT = {
    '0': 'Error Inesperado',
    '1': 'Aceptada',
    '2': 'En Proceso',
    '3': 'Terminada',
    '4': 'Error',
    '5': 'Rechazada',
    '6': 'Vencida',
}


def authenticate_request(fiel):
        auth = Authenticate(fiel)
        return auth.get_token()


class AddRequest(QDialog, requestDialog):
    def __init__(self, *args, empresa=False, fiel=False, **kwargs):
        super(AddRequest, self).__init__(*args, **kwargs)
        self.empresa = empresa
        self.fiel = fiel
        self.setupUi(self)
        self.setWindowTitle('Agregar Solicitud de Descatga')
        self.select_fiel.addItem(fiel.name)
        for w in (self.date_init, self.date_end):
            w.setDisplayFormat('ddMMyyyy')
            w.setCalendarPopup(True)
        self.setup_date()
        self.chk_issuer.clicked.connect(self.toggle_receiver)
        self.chk_receiver.clicked.connect(self.toggle_issuer)

    def toggle_receiver(self):
        self.chk_receiver.setEnabled(not (self.chk_issuer.isEnabled()))

    def toggle_issuer(self):
        self.chk_issuer.setEnabled(not (self.chk_receiver.isEnabled()))

    def setup_date(self):
        now = datetime.now() - timedelta(days=-1)
        self.date_init.setMinimumDate(QDate(2014, 1, 1))
        self.date_init.setMaximumDate(QDate(now.year, now.month, now.day))
        self.date_end.setMinimumDate(QDate(2014, 1, 2))
        self.date_init.setMaximumDate(QDate(now.year, now.month, now.day))

    def get_request_data(self):
        init_date = datetime(
            self.date_init.date().year(),
            self.date_init.date().month(),
            self.date_init.date().day()
        )
        end_date = datetime(
            self.date_end.date().year(),
            self.date_end.date().month(),
            self.date_end.date().day()
        )
        return {
            'name': self.txt_name.text(),
            'init_date': init_date,
            'end_date': end_date,
            'state': 'local',
            'fiel_id': self.fiel.id,
            'empresa_id': self.empresa.id,
            'issuer': self.chk_issuer.isChecked(),
            'receiver': self.chk_receiver.isChecked(),
        }

    def add_request(self):
        data = self.get_request_data()
        req = Request(**data)
        req.save_to_db()


class AddFiel(QDialog, fielDialog):
    def __init__(self, *args, empresa=False, **kwargs):
        super(AddFiel, self).__init__(*args, **kwargs)
        self.empresa = empresa
        self.setupUi(self)
        self.setWindowTitle("Agregar Fiel")
        self.mark_as_active.toggle()
        self.txt_empresa.setText('{} ({})'.format(self.empresa.name, self.empresa.rfc))
        self.txt_empresa.setReadOnly(True)
        self.btn_get_cer.clicked.connect(self.get_certificate)
        self.btn_get_key.clicked.connect(self.get_key)

    def get_certificate(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "Certificate Files (*.cer)",
            options=options,
        )
        self.txt_certificate.setText(file_name)

    def get_key(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "Key Files (*.key)",
            options=options,
        )
        self.txt_key.setText(file_name)

    def add_fiel(self):
        cer_path = self.txt_certificate.text()
        key_path = self.txt_key.text()
        passphrase = self.txt_password.text()
        if cer_path and key_path and passphrase:
            if os.path.isfile(cer_path) and os.path.isfile(key_path):
                with open(cer_path, 'rb') as f:
                    cer_der = f.read()

                with open(key_path, 'rb') as f:
                    key_der = f.read()

                fiel = Certificates(cer_der, key_der, passphrase)

                dates = fiel.get_cert_dates()
                data = {
                    'name': fiel.get_serial(),
                    'cer_pem': fiel.get_cer_pem(),
                    'key_pem': fiel.get_key_pem(passphrase),
                    'passphrase': passphrase,
                    'active': self.mark_as_active.isChecked(),
                    'date_init': dates['start'],
                    'date_end': dates['end'],
                    'empresa_id': self.empresa.id,
                }

                fiel_o = Fiel(**data)
                fiel_o.save_to_db()


class AddEmpresa(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(AddEmpresa, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Agregar Empresa")

    def add_empresa(self):
        name = False
        rfc = False
        if self.txt_name.text():
            name = self.txt_name.text()
        if self.txt_rfc.text():
            rfc = self.txt_rfc.text()

        if not name or not rfc:
            print('Debe Insertar un Nombre y RFC.')
        else:
            e = Empresa.find_by_rfc(rfc)
            if e:
                print('Ya existe una empresa con ese RFC.')
            else:
                e = Empresa(rfc=rfc, name=name)
                print('Agregando {}, {}'.format(name, rfc))
                e.save_to_db()


class ReqPackagesWindow(QMainWindow, req_packMW):
    def __init__(self, controller, req, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.controller = controller
        self.setWindowTitle('CFDi Blacklist - Paquetes')
        self.tbl_packages.setColumnHidden(2, True)
        self.btn_search.clicked.connect(self.get_dir)
        self.btn_download.clicked.connect(self.download_package)
        self.disable_buttons()
        if req:
            self.req = req
            self.load_data()
            self.load_packages()

    def load_data(self):
        self.select_request.clear()
        self.select_request.addItems([self.req.name])

    def load_packages(self):
        packages = Package.get_by_request_id(self.req.id)
        self.tbl_packages.setRowCount(len(packages))
        for i, p in enumerate(packages):
            self.tbl_packages.setItem(i, 0, QTableWidgetItem(str(p.uuid_pack)))
            self.tbl_packages.setItem(i, 1, QTableWidgetItem(str(p.downloaded and 'Si' or 'No')))
            self.tbl_packages.setItem(i, 2, QTableWidgetItem(str(p.id)))
        self.tbl_packages.itemClicked.connect(self.enable_buttons)

    def enable_buttons(self):
        self.btn_search.setEnabled(True)
        self.btn_download.setEnabled(True)

    def disable_buttons(self):
        self.btn_search.setEnabled(False)
        self.btn_download.setEnabled(False)

    def get_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            options=options,
        )
        self.txt_folder.setText(dir_name)

    def get_selected_package(self):
        id_pack = self.tbl_packages.item(
            self.tbl_packages.currentRow(),
            2
        ).text()
        return Package.find_by_id(id_pack)

    def download_package(self):
        pack = self.get_selected_package()
        if not pack:
            return
        pack_data = False
        if not pack.downloaded:
            pack_data = self.download_package_sat(pack)
        else:
            pack_data = base64.b64encode(pack.pack_data)
        
        if pack_data:
            self.store_data(pack_data)

    def download_package_sat(self, pack):
        f = Certificates(
            self.req.fiel.cer_pem.encode('utf-8'),
            self.req.fiel.key_pem.encode('utf-8'),
            self.req.fiel.passphrase,
            pem=True
        )
        if pack and f:
            print('Intentando Descarga')
            token = authenticate_request(f)
            download = DownloadCFDi(f)
            data = download.download_package(token, self.req.empresa.rfc, pack.uuid_pack)
            print(data.get('cod_estatus'))
            print(data.get('mensaje'))
            pack_data = data.get('paquete_b64')
            
            pack.update({
                'pack_data': base64.b64decode(pack_data),
                'downloaded': True
            })
            return pack_data

    def get_file_path(self, file_name):
        return '{}{}{}.zip'.format(
            self.txt_folder.text(),
            os.path.sep,
            file_name,
        )

    def store_data(self, pack_data):
        file_name = self.txt_name.text() and self.txt_name.text() or 'paquete_cfdi'
        file_path = self.get_file_path(file_name)
        i = 1
        while os.path.isfile(file_path):
            fn = '{}({})'.format(file_name, i)
            file_path = self.get_file_path(fn)
            i += 1
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(pack_data))
        print('Archivo guardado en Disco')


class EmpresaWindow(QMainWindow, empresaMW):
    def __init__(self, controller, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.controller = controller
        self.setWindowTitle('CFDi Blacklist')
        self.load_data()
        self.btn_add.clicked.connect(self.add_empresa)
        self.btn_delete.clicked.connect(self.delete_empresa)

    def load_data(self):
        empresas = s.query(Empresa).all()
        self.tbl_empresas.setRowCount(len(empresas))
        i = 0
        for empresa in empresas:
            self.tbl_empresas.setItem(i, 0, QTableWidgetItem(str(empresa.name)))
            self.tbl_empresas.setItem(i, 1, QTableWidgetItem(str(empresa.rfc)))
            i += 1

        self.tbl_empresas.doubleClicked.connect(self.edit_empresa)

    def delete_empresa(self):
        for current in self.tbl_empresas.selectedItems():
            rfc_empresa = self.tbl_empresas.item(current.row(), 1).text()
            e = Empresa.find_by_rfc(rfc_empresa)
            e.delete()
        self.load_data()

    def edit_empresa(self):
        rfc_empresa = self.tbl_empresas.item(
            self.tbl_empresas.currentRow(),
            1
        ).text()
        e = Empresa.find_by_rfc(rfc_empresa)
        self.controller.show_emp_fiel_window(e)

    def add_empresa(self):
        dlg = AddEmpresa(self)
        if dlg.exec_():
            dlg.add_empresa()
            self.load_data()
            self.controller.reload_main_window()

        else:
            print('Cancel!')


class EmpresaFielWindow(QMainWindow, empresa_fielMW):
    def __init__(self, controller, empresa, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.controller = controller
        self.empresa = empresa
        self.setWindowTitle('CFDi Blacklist')
        self.load_data()
        self.btn_add.clicked.connect(self.add_fiel)
        self.btn_delete.clicked.connect(self.delete_fiel)

    def load_data(self):
        empresa_txt = '{} ({})'.format(self.empresa.name, self.empresa.rfc)
        self.txt_empresa.setText(empresa_txt)
        self.txt_empresa.setReadOnly(True)
        fiels = Fiel.get_by_empresa_id(self.empresa.id)
        self.tbl_fiel.setRowCount(len(fiels))
        i = 0
        fmt = '%d/%m/%Y'
        for fiel in fiels:
            self.tbl_fiel.setItem(i, 0, QTableWidgetItem(str(fiel.name)))
            self.tbl_fiel.setItem(i, 1, QTableWidgetItem(str(fiel.date_init.strftime(fmt))))
            self.tbl_fiel.setItem(i, 2, QTableWidgetItem(str(fiel.date_end.strftime(fmt))))
            self.tbl_fiel.setItem(i, 3, QTableWidgetItem(str(fiel.active and 'Si' or 'No')))
        self.tbl_fiel.doubleClicked.connect(self.print_fiel_pems)

    def add_fiel(self):
        dlg = AddFiel(self, empresa=self.empresa)
        if dlg.exec_():
            dlg.add_fiel()
            self.load_data()

        else:
            print('Cancel!')

    def get_selected_fiel(self):
        serial = self.tbl_fiel.item(
            self.tbl_fiel.currentRow(),
            0
        ).text()
        return Fiel.find_by_name(serial)

    def delete_fiel(self):
        fiel = self.get_selected_fiel()
        fiel.delete()
        self.load_data()

    def print_fiel_pems(self):
        fiel = self.get_selected_fiel()
        if fiel:
            # print(fiel.cer_pem)
            print(fiel.key_pem)


class MainWindow(QMainWindow, mainWindow):
    def __init__(self, controller, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.controller = controller
        # Descarga
        self.empresa = False
        self.tbl_request.setColumnHidden(7, True)
        self.load_data()
        self.btn_load_empresa.clicked.connect(self.load_empresa)
        self.btn_add_request.clicked.connect(self.add_request)
        self.actionEmpresas.triggered.connect(self.controller.show_emp_window)
        self.btn_delete_request.clicked.connect(self.delete_request)
        self.btn_start.clicked.connect(self.start_request)
        self.btn_check.clicked.connect(self.check_request)
        self.btn_download.clicked.connect(self.download_package)
        self.disable_buttons()
        # Consulta
        self.btn_folder.clicked.connect(self.search_cfdi_folder)
        self.btn_report.clicked.connect(self.search_report_folder)
        self.btn_process_dir.clicked.connect(self.process_dir)
        self.btn_update.clicked.connect(self.update_blacklist)
        self.txt_cfdi_dir.setReadOnly(True)
        self.txt_dir_report.setReadOnly(True)
        self.text_result.setReadOnly(True)
        self.txt_report_name.setText('reporte_cfdi')

    def process_folder(self, folder_path):
        errors = 0
        lines = []
        for root, _, files in os.walk(folder_path):
            for name in files:
                if name.split('.')[-1].upper() in ('XML'):
                    filename = '{}{}{}'.format(root, os.sep, name)
                    lines.append('-\n')
                    lines.append('- Consultando {}'.format(filename))
                    err, line = self.process_xml_file(filename)
                    errors += err
                    lines.append(line)
        return errors, lines


    def process_xml_file(self, filename):
        print('Buscando problemas en {}\n'.format(filename))
        fileCfdi = CfdiXml(filename)
        rfcs = [fileCfdi.get_rfc_emisor(), fileCfdi.get_rfc_receptor()]
        blacklist = Blacklist.find_by_rfcs(rfcs=rfcs)
        e = 0
        if blacklist:
            for bl in blacklist:
                archivo = bl.get('defi') and 'Definitivos' or 'Presuntos'
                e = 1
                line = 'Problema con archivo {}\nContiene RFC: {} de la persona {}\n' \
                    'El cual esta indicado en la línea {} del archivo de {} del SAT\n' \
                    .format(
                        filename,
                        bl.get('rfc'),
                        bl.get('name'),
                        bl.get('csv_line'),
                        archivo)
                print(line)
        else:
            line = 'Ningún problema detectado.'
            print(line)
        print('-----------------------------------------\n')
        return e, line

    def write_report(self, lines):
        report_name = '{}{}{}.txt'.format(
            self.txt_dir_report.text(),
            os.path.sep,
            self.txt_report_name.text(),
        )
        with open(report_name, 'w') as f:
            f.write('\n'.join(lines))

    def process_dir(self):
        print('Procesando Archivos')
        folder_path = self.txt_cfdi_dir.text()

        if os.path.isdir(folder_path):
            e, l = self.process_folder(folder_path)
            if e == 0:
                self.text_result.setPlainText(
                    'Procesamiento del Directorio completado, no se encontraron errores'
                )
            else:
                self.text_result.setPlainText(
                    'Procesamiento del Directorio completado, se encontraron {} ' \
                    'error(es). Consulte el reporte para más detalles.' \
                        .format(e)
                )

            if self.chk_report.isChecked():
                self.write_report(l)
        else:
            self.text_result.setPlainText('Error! El directorio seleccionado es inválido.')

    def update_blacklist(self):
        print('Actualizando la Base de Datos del SAT.')
        process_blacklist_update()
        print('Actualización Terminada Satisfactoriamente.')

    def search_cfdi_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            options=options,
        )
        self.txt_cfdi_dir.setText(dir_name)

    def search_report_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            options=options,
        )
        self.txt_dir_report.setText(dir_name)

    def disable_buttons(self):
        self.btn_add_request.setEnabled(False)
        self.btn_delete_request.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.btn_check.setEnabled(False)
        self.btn_download.setEnabled(False)

    def load_data(self):
        empresas = Empresa.find_all()
        if empresas:
            self.empresas = {'{} ({})'.format(e.name, e.rfc): e for e in empresas}
            emp_list = list(self.empresas.keys())
            self.select_empresa.clear()
            self.select_empresa.addItems(emp_list)

    def load_empresa(self):
        selected_emp = str(self.select_empresa.currentText())
        if selected_emp not in '':
            self.empresa = self.empresas.get(selected_emp)
            reqs = Request.get_by_empresa_id(self.empresa.id)
            self.tbl_request.setRowCount(len(reqs))
            for i, r in enumerate(reqs):
                self.tbl_request.setItem(i, 0, QTableWidgetItem(str(r.name)))
                self.tbl_request.setItem(i, 1, QTableWidgetItem(str(r.init_date)))
                self.tbl_request.setItem(i, 2, QTableWidgetItem(str(r.end_date)))
                self.tbl_request.setItem(i, 3, QTableWidgetItem(str(r.state)))
                self.tbl_request.setItem(i, 4, QTableWidgetItem(str(r.numero_cfdis or '-')))
                self.tbl_request.setItem(i, 5, QTableWidgetItem(str(r.estado_solicitud or '-')))
                self.tbl_request.setItem(i, 6, QTableWidgetItem(str(r.mensaje or '-')))
                self.tbl_request.setItem(i, 7, QTableWidgetItem(str(r.id)))
            if len(Fiel.get_by_empresa_id(self.empresa.id)) > 0:
                self.btn_add_request.setEnabled(True)
            self.tbl_request.itemClicked.connect(self.activate_request_buttons)

    def activate_request_buttons(self):
        self.btn_delete_request.setEnabled(True)
        self.btn_start.setEnabled(True)
        self.btn_check.setEnabled(True)
        self.btn_download.setEnabled(True)

    def add_request(self):
        fiel = Fiel.get_active_fiel(self.empresa.id)
        if not fiel:
            return
        dlg = AddRequest(self, empresa=self.empresa, fiel=fiel)
        if dlg.exec_():
            dlg.add_request()
            self.load_empresa()

        else:
            print('Cancel!')

    def get_selected_request(self):
        id_req = self.tbl_request.item(
            self.tbl_request.currentRow(),
            7
        ).text()
        return Request.find_by_id(id_req)

    def delete_request(self):
        req = self.get_selected_request()
        req.delete()
        self.disable_buttons()
        self.load_empresa()

    def get_start_attributes(self, req):
        return {
            'requester_rfc': req.empresa.rfc,
            'init_date': req.init_date,
            'end_date': req.end_date + timedelta(days=1),
            'issuer_rfc': req.issuer and req.empresa.rfc or None,
            'receiver_rfc': req.receiver and req.empresa.rfc or None,
            'req_type': 'CFDI',
        }

    def start_request(self):
        req = self.get_selected_request()
        if req.state != 'local':
            return
        f = Certificates(
            req.fiel.cer_pem.encode('utf-8'),
            req.fiel.key_pem.encode('utf-8'),
            req.fiel.passphrase,
            pem=True
        )
        sol = RequestDownload(f)
        req_attrs = self.get_start_attributes(req)
        req_attrs['token'] = authenticate_request(f)
        # print(req_attrs)
        print('Iniciando Solicitud de {} en el SAT'.format(req.name))
        data = sol.request_download(**req_attrs)
        print(data)
        values = {}
        if data.get('cod_estatus') == '5000':
            values['state'] = 'iniciada'
        if data.get('id_solicitud'):
            values['uuid_request'] = data['id_solicitud']
        if data.get('cod_estatus'):
            values['cod_estatus'] = data['cod_estatus']
        if data.get('mensaje'):
            values['mensaje'] = data['mensaje']
        req.update(values)
        self.load_empresa()

    def check_request(self):
        req = self.get_selected_request()
        print('Realizando verificación de: {}'.format(req.name))
        has_package = len(Package.get_by_request_id(req.id)) > 0 and True or False
        if req.state not in ('iniciada', 'verificada'):
            return
        fiel = Fiel.find_by_id(req.fiel_id)
        if not fiel:
            print('La solicitud no tiene una Fiel Válida')
            return
        f = Certificates(
            fiel.cer_pem.encode('utf-8'),
            fiel.key_pem.encode('utf-8'),
            fiel.passphrase,
            pem=True
        )
        check = RequestCheck(f)
        token = authenticate_request(f)
        data = check.check_request(token, self.empresa.rfc, req.uuid_request)
        print(data)
        values = {
            'state': 'verificada',
        }
        if data.get('cod_estatus'):
            values['cod_estatus'] = data['cod_estatus']
        if data.get('estado_solicitud'):
            if ESTADOS_SAT.get(data['estado_solicitud']):
                values['estado_solicitud'] = ESTADOS_SAT[data['estado_solicitud']]
            else:
                values['estado_solicitud'] = data['estado_solicitud']
        if data.get('codigo_estado_solicitud'):
            values['codigo_estado_solicitud'] = data['codigo_estado_solicitud']
        if data.get('numero_cfdis'):
            values['numero_cfdis'] = int(data['numero_cfdis'])
        if data.get('mensaje'):
            values['mensaje'] = data['mensaje']
        req.update(values)
        if not has_package:
            for paq in data.get('paquetes'):
                p = Package(uuid_pack=paq, request_id=req.id, downloaded=False)
                p.save_to_db()
        self.load_empresa()

    def download_package(self):
        req = self.get_selected_request()
        self.controller.show_package_window(req)


class Controller:
    def __init__(self):
        pass

    def show_main_window(self):
        self.window = MainWindow(self)
        self.window.setWindowTitle('CFDi Blacklist')
        self.window.show()

    def reload_main_window(self):
        self.window.load_data()

    def show_empresas_window(self):
        self.ui = EmpresaWindow(self)
        self.ui.setupUi(self.window)
        self.window.setWindowTitle('CFDi Blacklist')
        self.ui.load_data()
        self.ui.btn_add.clicked.connect(self.ui.add_empresa)
        self.ui.btn_delete.clicked.connect(self.ui.delete_empresa)
        self.window.show()

    def show_empresas_fiel_window(self, empresa):
        self.ui = EmpresaFielWindow(self, empresa)
        self.ui.setupUi(self.window)
        self.ui.setWindowTitle('CFDi Blacklist')
        self.ui.load_data()
        self.ui.btn_add.clicked.connect(self.ui.add_fiel)
        self.ui.btn_delete.clicked.connect(self.ui.delete_fiel)
        self.window.show()

    def show_emp_window(self):
        self.window_two = EmpresaWindow(self)
        self.window_two.show()

    def show_emp_fiel_window(self, e):
        self.window_two.close()
        self.window_three = EmpresaFielWindow(self, e)
        self.window_three.show()

    def show_package_window(self, req):
        self.window_two = ReqPackagesWindow(self, req)
        self.window_two.show()


if __name__ == '__main__':
    import sys
    try:
        s.query(Empresa).all()
        print('Base de Datos encontrada')
    except Exception:
        print('Creando BD')
        recreate_database()
    app = QApplication([])
    controller = Controller()
    controller.show_main_window()
    sys.exit(app.exec_())