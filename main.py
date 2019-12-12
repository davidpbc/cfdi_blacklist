from ui.main_ui import Ui_MainWindow as mainWindow
from ui.empresas_ui import Ui_mainWindow as empresaMW
from ui.empresa_fiel_ui import Ui_MainWindow as empresa_fielMW
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
from models.base import Session
from models.empresa import Empresa
from models.fiel import Fiel
from models.request import Request
from download.certificate import Certificates
from datetime import datetime, timedelta
import os

s = Session()


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
                    'key_pem': fiel.get_key_pem(),
                    'passphrase': self.txt_password.text(),
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

    def add_fiel(self):
        dlg = AddFiel(self, empresa=self.empresa)
        if dlg.exec_():
            dlg.add_fiel()
            self.load_data()

        else:
            print('Cancel!')

    def delete_fiel(self):
        print("Deleting Fiel")


class MainWindow(QMainWindow, mainWindow):
    def __init__(self, controller, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.controller = controller
        self.empresa = False
        self.load_data()
        self.btn_load_empresa.clicked.connect(self.load_empresa)
        self.btn_add_request.clicked.connect(self.add_request)
        self.actionEmpresas.triggered.connect(self.controller.show_emp_window)

    def load_data(self):
        empresas = s.query(Empresa).all()
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


class Controller:
    def __init__(self):
        pass

    def show_main_window(self):
        self.window = MainWindow(self)
        self.window.setWindowTitle('CFDi Blacklist')
        self.window.show()

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


if __name__ == '__main__':
    import sys
    app = QApplication([])
    controller = Controller()
    controller.show_main_window()
    sys.exit(app.exec_())