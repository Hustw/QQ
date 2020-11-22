from all_windows.Register import RgstForm
from settingconfig import *
from base64 import b64encode,b64decode
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from image_handle import setlabel_imgstr

class ModifyWindows(RgstForm):
    """
    修改资料界面类：
        继承父类（注册界面类全部属性和方法）
        重写初始化函数：
        重写视窗关闭函数
        重写注册函数
    """
    def __init__(self, info, sock, parent=None):
        """
        重写初始化函数：
            利用用户的原资料初始化资料输入控件
        """
        super(ModifyWindows, self).__init__(RgstForm)
        self.setWindowTitle("修改资料")
        self.s = sock
        self.info = info
        self.win = parent

        # 利用用户的原资料初始化资料输入控件
        setlabel_imgstr(info['image'],self.label_image,85)
        self.gender = info['gender']
        self.lineEdit_nickname.setText(info['nickname'])
        self.lineEdit_pswd.setText(info['password'])
        self.lineEdit_cfrmpwd.setText(info['password'])
        self.lineEdit_region_prov.setText(info['region_prov'])
        self.lineEdit_region_city.setText(info['region_city'])
        self.comboBox_birthday_year.setCurrentText(info['birthday'].split('-')[0])
        self.comboBox_birthday_month.setCurrentText(info['birthday'].split('-')[1])
        self.comboBox_birthday_day.setCurrentText(info['birthday'].split('-')[2])
        self.textEdit_signature.setText(info['style_sign'])
        if self.gender == '男':
            self.radioButton_male.toggle()
        if self.gender == '女':
            self.radioButton_female.toggle()
        if self.gender == '保密':
            self.radioButton_none.toggle()
            
    def closeEvent(self, event):
        """
        重写视窗关闭函数:
        父视窗修改资料界面重新使能（关闭修改视窗后可再次打开，且确保只能打开一个）
        """
        self.win.modify_is_show = False           

    def regist(self):
        """
        重写注册函数：
            确定修改资料询问
            规范用户输入
            向服务器发送修改资料请求和用户填写的资料
            提示修改资料成功
        """
        message = QMessageBox.question(self,"修改资料","确定要修改你的资料？",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)   # 确定修改资料询问
        if message == QMessageBox.No:
            self.close()
        nickname = self.lineEdit_nickname.text()
        if nickname == "":
            QMessageBox.warning(self, "提示", "昵称不能为空", QMessageBox.Yes)
            self.lineEdit_nickname.setFocus()
            return
        password = self.lineEdit_pswd.text()
        comfirmpw = self.lineEdit_cfrmpwd.text()
        if ' ' in password:
            QMessageBox.warning(self, "提示", "密码中不能有空格", QMessageBox.Yes)
            self.clear_pwd()
            return
        elif len(password) > 16 or len(password) < 6:
            QMessageBox.warning(self, "提示", "密码长度不符", QMessageBox.Yes)
            self.clear_pwd()
            return
        elif password != comfirmpw:
            QMessageBox.warning(self, "提示", "两次输入密码不同！", QMessageBox.Yes)
            self.clear_pwd()
            return          #规范用户输入
        else:
            region_prov = self.lineEdit_region_prov.text()
            region_city = self.lineEdit_region_city.text()
            bir_year = self.comboBox_birthday_year.currentText()
            bir_mon = self.comboBox_birthday_month.currentText()
            bir_day = self.comboBox_birthday_day.currentText()
            birthday = bir_year + '-' + bir_mon + '-' + bir_day
            style_sign = self.textEdit_signature.toPlainText()
            reg_dict = {'cmd': 'modify','uid': self.info['uid'],'img': self.imgstr,'nknm': nickname, 'pswd': password, 'gd': self.gender,
                        'bir': birthday, 'prv': region_prov, 'cty': region_city, 'sty': style_sign}
            reg_json = json.dumps(reg_dict, ensure_ascii=False)
            self.s.send(reg_json.encode())      #向服务器发送修改资料请求和用户填写的资料
            QMessageBox.information(self, "恭喜","修改资料成功" , QMessageBox.Yes)      #提示修改资料成功
            self.close()
            




        


