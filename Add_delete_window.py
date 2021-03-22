# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5.QtWidgets import QMessageBox, QDialog

from PyQt5 import QtCore, QtWidgets


class Intent_Dialog(QDialog):
    def __init__(self, type_oper, parent=None):
        super(Intent_Dialog, self).__init__(parent)
        self.intent_operation = type_oper
        self.name_intent = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(543, 210)
        Dialog.setStyleSheet("background-color:#F0E3E2;")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 70, 141, 31))
        self.label.setStyleSheet("font-family: Lemonade;\n"
                                 "font-size:16px;")
        self.label.setObjectName("label")
        self.name_line = QtWidgets.QLineEdit(Dialog)
        self.name_line.setGeometry(QtCore.QRect(170, 71, 351, 31))
        self.name_line.setStyleSheet("background-color: #F4E9ED;\n"
                                     "font-family: Lemonade;\n"
                                     "font-size:18px;")
        self.name_line.setObjectName("name_line")
        self.button_ok = QtWidgets.QPushButton(Dialog)
        self.button_ok.setGeometry(QtCore.QRect(60, 150, 160, 40))
        self.button_ok.setStyleSheet("background-color: #E6CFD7;\n"
                                     "font-family: Lemonade;\n"
                                     "font-size:16px;")
        self.button_ok.setObjectName("button_ok")
        self.button_cancel = QtWidgets.QPushButton(Dialog)
        self.button_cancel.setGeometry(QtCore.QRect(320, 150, 160, 40))
        self.button_cancel.setStyleSheet("background-color: #E6CFD7;\n"
                                         "font-family: Lemonade;\n"
                                         "font-size:16px;")
        self.button_cancel.setObjectName("button_cancel")

        self.button_cancel.clicked.connect(self.Dialog_Close)
        self.button_ok.clicked.connect(self.Enter_Intent)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "Название интента:"))
        self.button_ok.setText(_translate("Dialog", "ОК"))
        self.button_cancel.setText(_translate("Dialog", "Отмена"))

        if self.intent_operation == 'add':
            Dialog.setWindowTitle(_translate("Dialog", "Добавление нового интента"))
        else:
            Dialog.setWindowTitle(_translate("Dialog", "Удаление интента"))

    # Обработка нажатия на кнопку Cancel
    def Dialog_Close(self):
        self.close()

    # Обработка нажатия на кнопку OK
    def Enter_Intent(self):
        if not self.name_line.text():
            QMessageBox.critical(self, "Ошибка ", "Вы не ввели название интента.", QMessageBox.Ok)
        else:
            self.name_intent = self.name_line.text()
            self.close()