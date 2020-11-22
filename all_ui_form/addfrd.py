# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddFrd(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(637, 446)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 621, 431))
        self.tabWidget.setMaximumSize(QtCore.QSize(621, 16777215))
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setStyleSheet("QTabBar::tab{width:300px;height:30px;}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_add = QtWidgets.QWidget()
        self.tab_add.setObjectName("tab_add")
        self.pushButton_search = QtWidgets.QPushButton(self.tab_add)
        self.pushButton_search.setGeometry(QtCore.QRect(440, 40, 112, 34))
        self.pushButton_search.setObjectName("pushButton_search")
        self.lineEdit_index = QtWidgets.QLineEdit(self.tab_add)
        self.lineEdit_index.setGeometry(QtCore.QRect(40, 40, 361, 31))
        self.lineEdit_index.setObjectName("lineEdit_index")
        self.listWidget_search = QtWidgets.QListWidget(self.tab_add)
        self.listWidget_search.setGeometry(QtCore.QRect(40, 110, 541, 251))
        self.listWidget_search.setObjectName("listWidget_search")
        self.tabWidget.addTab(self.tab_add, "")
        self.tab_request = QtWidgets.QWidget()
        self.tab_request.setObjectName("tab_request")
        self.label_list = QtWidgets.QLabel(self.tab_request)
        self.label_list.setGeometry(QtCore.QRect(40, 40, 271, 21))
        self.label_list.setObjectName("label_list")
        self.listWidget_rqst = QtWidgets.QListWidget(self.tab_request)
        self.listWidget_rqst.setGeometry(QtCore.QRect(40, 70, 511, 311))
        self.listWidget_rqst.setObjectName("listWidget_rqst")
        self.tabWidget.addTab(self.tab_request, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_search.setText(_translate("Form", "搜索"))
        self.lineEdit_index.setPlaceholderText(_translate("Form", "请输入ID/昵称搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_add), _translate("Form", "添加好友"))
        self.label_list.setText(_translate("Form", "好友请求列表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_request), _translate("Form", "验证消息"))

