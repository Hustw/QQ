# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(785, 563)
        Form.setMinimumSize(QtCore.QSize(785, 563))
        Form.setMaximumSize(QtCore.QSize(785, 563))
        self.lineEdit_usrid = QtWidgets.QLineEdit(Form)
        self.lineEdit_usrid.setGeometry(QtCore.QRect(180, 110, 411, 41))
        self.lineEdit_usrid.setObjectName("lineEdit_usrid")
        self.lineEdit_usrid.setPlaceholderText("账号")

        self.lineEdit_pswd = QtWidgets.QLineEdit(Form)
        self.lineEdit_pswd.setGeometry(QtCore.QRect(180, 230, 411, 41))
        self.lineEdit_pswd.setObjectName("lineEdit_pswd")
        self.lineEdit_pswd.setEchoMode(QLineEdit.Password)
        self.lineEdit_pswd.setPlaceholderText("密码")

        self.pushButton_login = QtWidgets.QPushButton(Form)
        self.pushButton_login.setGeometry(QtCore.QRect(270, 410, 221, 51))
        self.pushButton_login.setCheckable(False)
        self.pushButton_login.setObjectName("pushButton_login")

        self.checkBox_rmbrpswd = QtWidgets.QCheckBox(Form)
        self.checkBox_rmbrpswd.setGeometry(QtCore.QRect(180, 300, 161, 81))
        self.checkBox_rmbrpswd.setObjectName("checkBox_rmbrpswd")

        self.checkBox_autologin = QtWidgets.QCheckBox(Form)
        self.checkBox_autologin.setGeometry(QtCore.QRect(450, 300, 131, 91))
        self.checkBox_autologin.setObjectName("checkBox_autologin")

        self.pushButton_regist = QtWidgets.QPushButton(Form)
        self.pushButton_regist.setGeometry(QtCore.QRect(10, 500, 111, 51))
        self.pushButton_regist.setCheckable(False)
        self.pushButton_regist.setObjectName("pushButton_regist")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_login.setText(_translate("Form", "登录"))
        self.checkBox_rmbrpswd.setText(_translate("Form", "记住密码"))
        self.checkBox_autologin.setText(_translate("Form", "自动登录"))
        self.pushButton_regist.setText(_translate("Form", "注册"))
