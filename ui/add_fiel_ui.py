# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_fiel.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(391, 334)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 290, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(130, 10, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.mark_as_active = QtWidgets.QCheckBox(Dialog)
        self.mark_as_active.setGeometry(QtCore.QRect(20, 250, 231, 23))
        self.mark_as_active.setObjectName("mark_as_active")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 351, 27))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.txt_empresa = QtWidgets.QLineEdit(self.layoutWidget)
        self.txt_empresa.setObjectName("txt_empresa")
        self.horizontalLayout.addWidget(self.txt_empresa)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 130, 351, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.txt_certificate = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txt_certificate.setObjectName("txt_certificate")
        self.horizontalLayout_3.addWidget(self.txt_certificate)
        self.btn_get_cer = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_get_cer.setObjectName("btn_get_cer")
        self.horizontalLayout_3.addWidget(self.btn_get_cer)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 170, 351, 27))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.txt_key = QtWidgets.QLineEdit(self.layoutWidget2)
        self.txt_key.setObjectName("txt_key")
        self.horizontalLayout_4.addWidget(self.txt_key)
        self.btn_get_key = QtWidgets.QPushButton(self.layoutWidget2)
        self.btn_get_key.setObjectName("btn_get_key")
        self.horizontalLayout_4.addWidget(self.btn_get_key)
        self.layoutWidget3 = QtWidgets.QWidget(Dialog)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 210, 351, 27))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.txt_password = QtWidgets.QLineEdit(self.layoutWidget3)
        self.txt_password.setObjectName("txt_password")
        self.horizontalLayout_5.addWidget(self.txt_password)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_6.setText(_translate("Dialog", "Agregar Fiel"))
        self.mark_as_active.setText(_translate("Dialog", "Marcar como Fiel Activa"))
        self.label_2.setText(_translate("Dialog", "Empresa"))
        self.label.setText(_translate("Dialog", "Certificado"))
        self.btn_get_cer.setText(_translate("Dialog", "Buscar"))
        self.label_3.setText(_translate("Dialog", "Llave"))
        self.btn_get_key.setText(_translate("Dialog", "Buscar"))
        self.label_4.setText(_translate("Dialog", "Contraseña"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
