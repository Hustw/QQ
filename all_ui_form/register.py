# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Rgst(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(705, 649)
        self.label_nickname = QtWidgets.QLabel(Form)
        self.label_nickname.setGeometry(QtCore.QRect(71, 137, 36, 18))
        self.label_nickname.setObjectName("label_nickname")
        self.label_pswd = QtWidgets.QLabel(Form)
        self.label_pswd.setGeometry(QtCore.QRect(71, 500, 36, 18))
        self.label_pswd.setObjectName("label_pswd")
        self.label_cfrmpwd = QtWidgets.QLabel(Form)
        self.label_cfrmpwd.setGeometry(QtCore.QRect(71, 540, 72, 18))
        self.label_cfrmpwd.setObjectName("label_cfrmpwd")
        self.lineEdit_nickname = QtWidgets.QLineEdit(Form)
        self.lineEdit_nickname.setGeometry(QtCore.QRect(152, 137, 193, 24))
        self.lineEdit_nickname.setObjectName("lineEdit_nickname")
        self.lineEdit_pswd = QtWidgets.QLineEdit(Form)
        self.lineEdit_pswd.setGeometry(QtCore.QRect(152, 500, 193, 24))
        self.lineEdit_pswd.setObjectName("lineEdit_pswd")
        self.lineEdit_cfrmpwd = QtWidgets.QLineEdit(Form)
        self.lineEdit_cfrmpwd.setGeometry(QtCore.QRect(152, 540, 193, 24))
        self.lineEdit_cfrmpwd.setObjectName("lineEdit_cfrmpwd")
        self.radioButton_male = QtWidgets.QRadioButton(Form)
        self.radioButton_male.setGeometry(QtCore.QRect(152, 177, 51, 22))
        self.radioButton_male.setObjectName("radioButton_male")
        self.radioButton_famale = QtWidgets.QRadioButton(Form)
        self.radioButton_famale.setGeometry(QtCore.QRect(326, 177, 51, 22))
        self.radioButton_famale.setObjectName("radioButton_famale")
        self.label_gender = QtWidgets.QLabel(Form)
        self.label_gender.setGeometry(QtCore.QRect(71, 177, 36, 18))
        self.label_gender.setObjectName("label_gender")
        self.pushButton_cancel = QtWidgets.QPushButton(Form)
        self.pushButton_cancel.setGeometry(QtCore.QRect(70, 580, 112, 34))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.radioButton_none = QtWidgets.QRadioButton(Form)
        self.radioButton_none.setGeometry(QtCore.QRect(500, 177, 69, 22))
        self.radioButton_none.setObjectName("radioButton_none")
        self.label_region = QtWidgets.QLabel(Form)
        self.label_region.setGeometry(QtCore.QRect(71, 214, 36, 18))
        self.label_region.setObjectName("label_region")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(-390, 670, 113, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_region_prov = QtWidgets.QLineEdit(Form)
        self.lineEdit_region_prov.setGeometry(QtCore.QRect(152, 214, 193, 24))
        self.lineEdit_region_prov.setObjectName("lineEdit_region_prov")
        self.lineEdit_region_city = QtWidgets.QLineEdit(Form)
        self.lineEdit_region_city.setGeometry(QtCore.QRect(384, 214, 193, 24))
        self.lineEdit_region_city.setObjectName("lineEdit_region_city")
        self.label_region_prov = QtWidgets.QLabel(Form)
        self.label_region_prov.setGeometry(QtCore.QRect(354, 214, 18, 18))
        self.label_region_prov.setObjectName("label_region_prov")
        self.label_region_city = QtWidgets.QLabel(Form)
        self.label_region_city.setGeometry(QtCore.QRect(586, 214, 18, 18))
        self.label_region_city.setObjectName("label_region_city")
        self.label_signature = QtWidgets.QLabel(Form)
        self.label_signature.setGeometry(QtCore.QRect(71, 293, 72, 18))
        self.label_signature.setObjectName("label_signature")
        self.textEdit_signature = QtWidgets.QTextEdit(Form)
        self.textEdit_signature.setGeometry(QtCore.QRect(152, 293, 421, 192))
        self.textEdit_signature.setObjectName("textEdit_signature")
        self.label_birthday = QtWidgets.QLabel(Form)
        self.label_birthday.setGeometry(QtCore.QRect(71, 254, 36, 18))
        self.label_birthday.setObjectName("label_birthday")
        self.comboBox_birthday_month = QtWidgets.QComboBox(Form)
        self.comboBox_birthday_month.setGeometry(QtCore.QRect(300, 254, 99, 24))
        self.comboBox_birthday_month.setObjectName("comboBox_birthday_month")
        self.comboBox_birthday_day = QtWidgets.QComboBox(Form)
        self.comboBox_birthday_day.setGeometry(QtCore.QRect(465, 254, 99, 24))
        self.comboBox_birthday_day.setObjectName("comboBox_birthday_day")
        self.label_birthday_month = QtWidgets.QLabel(Form)
        self.label_birthday_month.setGeometry(QtCore.QRect(420, 254, 18, 18))
        self.label_birthday_month.setObjectName("label_birthday_month")
        self.label_birthday_day = QtWidgets.QLabel(Form)
        self.label_birthday_day.setGeometry(QtCore.QRect(586, 254, 18, 18))
        self.label_birthday_day.setObjectName("label_birthday_day")
        self.pushButton_regist = QtWidgets.QPushButton(Form)
        self.pushButton_regist.setGeometry(QtCore.QRect(465, 580, 112, 34))
        self.pushButton_regist.setObjectName("pushButton_regist")
        self.pushButton_image = QtWidgets.QPushButton(Form)
        self.pushButton_image.setGeometry(QtCore.QRect(71, 50, 91, 34))
        self.pushButton_image.setObjectName("pushButton_image")
        self.label_image = QtWidgets.QLabel(Form)
        self.label_image.setGeometry(QtCore.QRect(200, 40, 81, 18))
        self.label_image.setObjectName("label_image")
        self.label_birthday_year = QtWidgets.QLabel(Form)
        self.label_birthday_year.setGeometry(QtCore.QRect(260, 254, 31, 20))
        self.label_birthday_year.setObjectName("label_birthday_year")
        self.comboBox_birthday_year = QtWidgets.QComboBox(Form)
        self.comboBox_birthday_year.setGeometry(QtCore.QRect(152, 254, 99, 24))
        self.comboBox_birthday_year.setObjectName("comboBox_birthday_year")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_nickname.setText(_translate("Form", "昵称"))
        self.label_pswd.setText(_translate("Form", "密码"))
        self.label_cfrmpwd.setText(_translate("Form", "确定密码"))
        self.lineEdit_nickname.setPlaceholderText(_translate("Form", "请输入昵称"))
        self.lineEdit_pswd.setPlaceholderText(_translate("Form", "6-12位字母或数字"))
        self.lineEdit_cfrmpwd.setPlaceholderText(_translate("Form", "请再次输入密码 "))
        self.radioButton_male.setText(_translate("Form", "男"))
        self.radioButton_famale.setText(_translate("Form", "女"))
        self.label_gender.setText(_translate("Form", "性别"))
        self.pushButton_cancel.setText(_translate("Form", "取消"))
        self.radioButton_none.setText(_translate("Form", "保密"))
        self.label_region.setText(_translate("Form", "地区"))
        self.label_region_prov.setText(_translate("Form", "省"))
        self.label_region_city.setText(_translate("Form", "市"))
        self.label_signature.setText(_translate("Form", "个性签名"))
        self.label_birthday.setText(_translate("Form", "生日"))
        self.label_birthday_month.setText(_translate("Form", "月"))
        self.label_birthday_day.setText(_translate("Form", "日"))
        self.pushButton_regist.setText(_translate("Form", "确定"))
        self.pushButton_image.setText(_translate("Form", "上传头像"))
        self.label_image.setText(_translate("Form", "TextLabel"))
        self.label_birthday_year.setText(_translate("Form", "年"))

