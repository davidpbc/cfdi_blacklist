# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'empresa_fiel.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(646, 327)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tbl_fiel = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl_fiel.setGeometry(QtCore.QRect(10, 60, 631, 181))
        self.tbl_fiel.setObjectName("tbl_fiel")
        self.tbl_fiel.setColumnCount(4)
        self.tbl_fiel.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_fiel.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_fiel.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_fiel.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_fiel.setHorizontalHeaderItem(3, item)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 631, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txt_empresa = QtWidgets.QLineEdit(self.widget)
        self.txt_empresa.setObjectName("txt_empresa")
        self.horizontalLayout.addWidget(self.txt_empresa)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(230, 250, 186, 27))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_add = QtWidgets.QPushButton(self.widget1)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_2.addWidget(self.btn_add)
        self.btn_delete = QtWidgets.QPushButton(self.widget1)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_2.addWidget(self.btn_delete)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 646, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tbl_fiel.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nombre"))
        item = self.tbl_fiel.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Inicio"))
        item = self.tbl_fiel.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Fin"))
        item = self.tbl_fiel.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Activo"))
        self.label.setText(_translate("MainWindow", "Empresa"))
        self.btn_add.setText(_translate("MainWindow", "Agregar"))
        self.btn_delete.setText(_translate("MainWindow", "Quitar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
