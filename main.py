from ui.empresas_ui import Ui_mainWindow as empresaMW
from ui.empresa_fiel_ui import Ui_MainWindow as empresa_fielMW
from ui.add_empresa_ui import Ui_Dialog
from ui.add_fiel_ui import Ui_Dialog as fielDialog
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
from download.certificate import Certificates
import os

s = Session()


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

    def print_empresa(self):
        print('\n')
        rfc_empresa = self.tbl_empresas.item(
            self.tbl_empresas.currentRow(),
            1
        ).text()
        e = Empresa.find_by_rfc(rfc_empresa)
        print("Empresa Seleccionada: {}\nRFC: {}".format(e.name, e.rfc))

    def edit_empresa(self):
        rfc_empresa = self.tbl_empresas.item(
            self.tbl_empresas.currentRow(),
            1
        ).text()
        e = Empresa.find_by_rfc(rfc_empresa)
        self.controller.show_empresas_fiel_window(e)

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


class Controller:
    def __init__(self):
        self.window = QMainWindow()

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


if __name__ == '__main__':
    import sys
    app = QApplication([])
    controller = Controller()
    controller.show_empresas_window()
    sys.exit(app.exec_())