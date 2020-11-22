import sys
from all_ui_form.login import Ui_Form
from all_windows.Register import RgstForm
from all_windows.QQWindow import QQWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket
from settingconfig import *
import json


class LoginForm(QMainWindow, Ui_Form):
    """
    登录界面类：
        控件类型：
            账号，密码行编辑器
            登录，注册按钮
            自动登录，记住密码多选框
        方法：
            登录初始化
            自动登录
            点击登录
            保存登录信息
            点击注册
    """
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("QQ")
        self.s = socket.socket()  # 创建客户端套接字
        self.host = HOST
        self.port = PORT
        self.s.connect((self.host, self.port))  # 连接服务器
        print(self.s.recv(BUFFSIZE).decode())

        self.usrid = ''
        self.timer = QTimer()  # 创建定时器
        self.pushButton_login.clicked.connect(self.Qlogin)  # 点击-登录
        self.pushButton_regist.clicked.connect(self.Register)  # 点击-注册
        self.initlogin()  # 初始化登录信息
        self.reg = RgstForm(self.s)  # 创建注册界面

    def closeEvent(self, event):
        self.s.close()

    def initlogin(self):
        """
        读注册表文件初始化信息
        """
        settings = QSettings("config.ini", QSettings.IniFormat)
        usrid = settings.value('userid')
        psswd = settings.value('password')
        rmbrpswd = settings.value('rememberpassword')
        autologin = settings.value('autologin')
        self.lineEdit_usrid.setText(usrid)
        if rmbrpswd == 'true':
            # 记住密码
            self.lineEdit_pswd.setText(psswd)
            self.checkBox_rmbrpswd.setChecked(True)
        if autologin == 'true':
            # 自动登录
            self.checkBox_autologin.setChecked(True)
            self.timer.timeout.connect(self.autolog)
            self.timer.setSingleShot(True)
            self.timer.start(2000)
        print('inital success')

    def autolog(self):
        """
        自动登录
        """
        if self.checkBox_autologin.isChecked():
            self.Qlogin()

    def Qlogin(self):
        """
        登录
        """
        self.usrid = self.lineEdit_usrid.text()
        psswd = self.lineEdit_pswd.text()
        log_dict = {'cmd': 'log', 'uid': self.usrid, 'pwd': psswd}
        log_json = json.dumps(log_dict)
        self.s.send(log_json.encode())
        feedback = self.s.recv(BUFFSIZE).decode()
        if feedback == "True":
            self.savelogin()
            jinfo = self.s.recv(BUFFSIZE).decode()
            info = json.loads(jinfo)
            QMessageBox.information(self, "恭喜", "登陆成功！",
                                    QMessageBox.Yes)
            self.hide() #隐藏登录窗口
            self.qqmwd = QQWindow(info, self.s)  # 创建并初始化主界面
            self.qqmwd.show()
        elif feedback == "Online":
            QMessageBox.warning(self, "提示", "当前账号已经在线！\n请勿重复登录",
                                QMessageBox.Yes)
        elif feedback == "False":
            QMessageBox.warning(self, "提示", "账号名或密码错误！",
                                QMessageBox.Yes)
            self.lineEdit_pswd.clear()
            self.lineEdit_pswd.setFocus()
            self.savelogin()

    def savelogin(self):
        """
        保存登录信息
        """
        settings = QSettings("config.ini", QSettings.IniFormat)
        settings.setValue("userid", self.lineEdit_usrid.text())
        settings.setValue("password", self.lineEdit_pswd.text())
        if self.checkBox_autologin.isChecked():
            settings.setValue("rememberpassword", True)
        else:
            settings.setValue("rememberpassword", self.checkBox_rmbrpswd.isChecked())
        settings.setValue("autologin", self.checkBox_autologin.isChecked())

    def Register(self):
        """
        注册账号
        """
        self.reg.show() #显示注册界面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginWin = LoginForm()
    loginWin.show()
    sys.exit(app.exec_())