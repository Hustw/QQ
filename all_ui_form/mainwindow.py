# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Mainwindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(585, 688)
        self.label_image = QtWidgets.QLabel(Form)
        self.label_image.setGeometry(QtCore.QRect(160, 60, 81, 18))
        self.label_image.setObjectName("label_image")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(150, 140, 381, 541))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget_friendlist = QtWidgets.QTreeWidget(self.layoutWidget)
        self.treeWidget_friendlist.setObjectName("treeWidget_friendlist")
        self.treeWidget_friendlist.headerItem().setText(0, "1")
        self.gridLayout.addWidget(self.treeWidget_friendlist, 0, 0, 1, 3)
        self.pushButton_add = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.gridLayout.addWidget(self.pushButton_add, 1, 0, 1, 1)
        self.pushButton_modify = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_modify.setObjectName("pushButton_modify")
        self.gridLayout.addWidget(self.pushButton_modify, 1, 1, 1, 1)
        self.pushButton_files = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_files.setObjectName("pushButton_files")
        self.gridLayout.addWidget(self.pushButton_files, 1, 2, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(260, 30, 83, 101))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_nickname = QtWidgets.QLabel(self.layoutWidget1)
        self.label_nickname.setObjectName("label_nickname")
        self.verticalLayout.addWidget(self.label_nickname)
        self.label_signature = QtWidgets.QLabel(self.layoutWidget1)
        self.label_signature.setObjectName("label_signature")
        self.verticalLayout.addWidget(self.label_signature)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_image.setText(_translate("Form", "TextLabel"))
        self.pushButton_add.setText(_translate("Form", "PushButton"))
        self.pushButton_modify.setText(_translate("Form", "PushButton"))
        self.pushButton_files.setText(_translate("Form", "PushButton"))
        self.label_nickname.setText(_translate("Form", "TextLabel"))
        self.label_signature.setText(_translate("Form", "TextLabel"))

