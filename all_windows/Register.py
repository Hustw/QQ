from all_ui_form.register import Ui_Rgst
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from settingconfig import *
from image_handle import imgpath2imgstr,setlabel_imgpath
import json

class RgstForm(QMainWindow, Ui_Rgst):
    """
    注册界面类：
        控件类型：
            上传头像按钮，头像显示标签
            昵称行编辑器
            性别单选器
            地区省、市行编辑器
            生日（年/月/日）下拉选择框
            个性签名多行编辑器
            密码、确认密码行编辑器
        方法：
            选择上传头像
            生日（年/月/日）下拉选择框初始化
            根据年份选择，修改月份-天数映射（判别是否选择年份为闰年，闰年2月为29天）
            根据月份选择，更新天数下拉窗选择项
            性别单选设置
            密码编辑框清除（两次密码不一致）
            注册函数
    """
    def __init__(self, sock, parent=None):
        super(RgstForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("注册账号")
        self.gender = '保密'
        self.s = sock

        default_path='./images/default.jpg'     #如果用户没有选择头像，就使用default.jpg
        self.imgstr = imgpath2imgstr(default_path)

        self.day_dict = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30,
                         '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}   #月份天数映射

        self.pushButton_image.clicked.connect(self.choose_image)
        self.radioButton_male.toggled.connect(self.change_gender_male)
        self.radioButton_famale.toggled.connect(self.change_gender_female)
        self.radioButton_none.toggled.connect(self.change_gender_unkn)
        
        self.pushButton_regist.clicked.connect(self.regist)
        self.pushButton_cancel.clicked.connect(self.close)
        self.init_combox()
        self.comboBox_birthday_month.currentIndexChanged.connect(self.month_changed)
        self.comboBox_birthday_year.currentIndexChanged.connect(self.year_changed)


    def choose_image(self):
        """
        选择上传头像
        """
        fname = QFileDialog.getOpenFileName(self, '选择图片','./images/', "JPEG Files(*.jpg);;PNG Files(*.png)")
        setlabel_imgpath(fname[0],self.label_image,85)  #选择图片显示
        self.imgstr = imgpath2imgstr(fname[0])  #转化图片为数据库支持格式
        
    def init_combox(self):
        """
        生日下拉框初始化
        """
        self.comboBox_birthday_year.addItems([str(i) for i in range(1970, 2021)])
        self.comboBox_birthday_month.addItems([str(i) for i in range(1, 13)])
        self.comboBox_birthday_day.addItems([str(i) for i in range(1, self.day_dict['1']+1)])

    def year_changed(self):
        """
        根据年份选择，修改月份-天数映射
        """
        year = self.comboBox_birthday_year.currentText()
        if int(year) % 4 == 0:
            if int(year) % 100 != 0 or int(year) % 400 == 0:
                self.day_dict['2'] = 29     #闰年2月为29天
            else:
                self.day_dict['2'] = 28
        else:
            self.day_dict['2'] = 28
        self.month_changed()

    def month_changed(self):
        """
        根据月份选择，更新天数下拉窗选择项
        """
        month = self.comboBox_birthday_month.currentText()
        self.comboBox_birthday_day.clear()
        self.comboBox_birthday_day.addItems([str(i) for i in range(1, self.day_dict[month]+1)])

    # 性别单选设置
    def change_gender_male(self):
        self.gender = '男'

    def change_gender_female(self):
        self.gender = '女'

    def change_gender_unkn(self):
        self.gender = '保密'

    def clear_pwd(self):
        """
        密码编辑框清除
        """
        self.lineEdit_pswd.clear()
        self.lineEdit_cfrmpwd.clear()
        self.lineEdit_pswd.setFocus()

    def regist(self):
        """
        注册函数：
            规范用户输入
            向服务器发送注册请求和用户填写的资料
            接受服务器返回分配的用户ID
        """
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
            return                 #规范用户输入
        else:
            region_prov = self.lineEdit_region_prov.text()
            region_city = self.lineEdit_region_city.text()
            bir_year = self.comboBox_birthday_year.currentText()
            bir_mon = self.comboBox_birthday_month.currentText()
            bir_day = self.comboBox_birthday_day.currentText()
            birthday = bir_year + '-' + bir_mon + '-' + bir_day
            style_sign = self.textEdit_signature.toPlainText()
            reg_dict = {'cmd': 'reg', 'img': self.imgstr,'nknm': nickname, 'pswd': password, 'gd': self.gender,
                        'bir': birthday, 'prv': region_prov, 'cty': region_city, 'sty': style_sign}
            reg_json = json.dumps(reg_dict, ensure_ascii=False)     #向服务器传送注册请求和用户填写的资料
            self.s.send(reg_json.encode())
            rid = self.s.recv(BUFFSIZE).decode()
            QMessageBox.information(self, "恭喜", "注册成功\n您的ID是%s" % rid, QMessageBox.Yes)    #打印提示分配的用户注册ID
            self.close()