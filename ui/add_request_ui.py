# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_request.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 273)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 220, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(70, 10, 249, 22))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(250, 130, 123, 28))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.date_end = QtWidgets.QDateEdit(self.layoutWidget)
        self.date_end.setObjectName("date_end")
        self.horizontalLayout.addWidget(self.date_end)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 130, 139, 28))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.date_init = QtWidgets.QDateEdit(self.layoutWidget1)
        self.date_init.setObjectName("date_init")
        self.horizontalLayout_2.addWidget(self.date_init)
        self.layoutWidget2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 90, 371, 27))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.txt_name = QtWidgets.QLineEdit(self.layoutWidget2)
        self.txt_name.setObjectName("txt_name")
        self.horizontalLayout_3.addWidget(self.txt_name)
        self.layoutWidget3 = QtWidgets.QWidget(Dialog)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 50, 371, 27))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.layoutWidget3)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.select_fiel = QtWidgets.QComboBox(self.layoutWidget3)
        self.select_fiel.setObjectName("select_fiel")
        self.horizontalLayout_4.addWidget(self.select_fiel)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 180, 371, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.chk_issuer = QtWidgets.QCheckBox(self.widget)
        self.chk_issuer.setObjectName("chk_issuer")
        self.horizontalLayout_5.addWidget(self.chk_issuer)
        self.chk_receiver = QtWidgets.QCheckBox(self.widget)
        self.chk_receiver.setObjectName("chk_receiver")
        self.horizontalLayout_5.addWidget(self.chk_receiver)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "Solicitud de Descarga Masiva"))
        self.label_4.setText(_translate("Dialog", "Fin"))
        self.label_3.setText(_translate("Dialog", "Inicio"))
        self.label_2.setText(_translate("Dialog", "Nombre"))
        self.label.setText(_translate("Dialog", "Fiel"))
        self.chk_issuer.setText(_translate("Dialog", "Emisor"))
        self.chk_receiver.setText(_translate("Dialog", "Receptor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
