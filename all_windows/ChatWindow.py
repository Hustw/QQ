from all_ui_form.chat import Ui_Chat
from PyQt5.QtWidgets import *
import json
from datetime import datetime
from PyQt5.QtGui import *
from queue import Queue
from MyThread import *
from image_handle import *


class ChatWindow(QMainWindow, Ui_Chat):
    """
    聊天界面类：
        控件：
            好友昵称label
            好友生日label
            好友个性签名label
            好友地区label
            好友头像label
            小图片icon
            发送按钮
            聊天浏览框textBrowser
        重要属性：
            self.q_cache            聊天记录本地缓存
            self.get_queue_tread    读取接受消息队列线程
        初始化：
            好友资料显示到控件
            聊天浏览框textBrowser滚动到底部
        方法:
            发送消息
            接受消息
            关闭事件函数
    """
    def __init__(self, parent_window, sock, my_info, frd_info, q, parent=None):
        super(ChatWindow, self).__init__(parent)
        self.setupUi(self)
        self.s = sock  # 父窗口套接字
        self.frd_info = frd_info  # 好友信息
        self.q = q  # 好友消息队列
        self.parent_window = parent_window  # 父窗口对象
        self.q_cache = Queue(1024)  # 聊天记录的本地缓存
        self.q_cache.put({'name': '', 'time': '', 'txt': ''})  # 第一个要被吃掉
        self.setWindowTitle(self.frd_info['nickname'])
        self.my_info = my_info
        self.label_nickname.setText(self.frd_info['nickname'])
        self.label_birthday.setText(self.frd_info['birthday'])
        self.label_signature.setText(self.frd_info['style_sign'])
        self.label_region.setText(self.frd_info['region_prov'] + '省 '
                                  + self.frd_info['region_city'] + '市')
        self.pushButton.clicked.connect(self.send_msg)

        self.pushButton.setShortcut('ctrl+return')
        self.get_queue_tread = GetQueueTread(self.q)  # 创建读取队列线程
        self.get_queue_tread.get_signal.connect(self.recv_msg)  # 自定义队列读取信号连接展示读取消息槽函数
        self.get_queue_tread.start()

        setlabel_imgstr(self.frd_info['image'],self.label_image,150)
        img_Qt = imgstr2imgQt(self.frd_info['image'])
        pix = QPixmap(img_Qt)
        self.icon = QIcon()
        self.icon.addPixmap(pix)
        self.setWindowIcon(self.icon)
        self.setCentralWidget(self.layoutWidget)

        self.textBrowser.ensureCursorVisible()  # 游标可用
        cursor = self.textBrowser.textCursor()  # 设置游标
        pos = len(self.textBrowser.toPlainText())  # 获取文本尾部的位置
        cursor.setPosition(pos)  # 游标位置设置为尾部
        self.textBrowser.setTextCursor(cursor)  # 滚动到游标位置


    def closeEvent(self, event):
        """
        重写关闭事件函数:
        窗口关闭后关闭队列读取线程并将双方聊天记录缓存写入消息队列
        """
        self.get_queue_tread.working = False
        while not self.q_cache.empty():
            self.q.put(self.q_cache.get())
        # 删除父窗口界面中聊天窗口字典里该好友的聊天窗口
        del self.parent_window.window_dict[self.frd_info['uid']]

    def send_msg(self):
        """
        发送消息：
        将发送消息及附加信息（发送者、时间）打印在聊天浏览框textBrowser
        向服务器发送聊天指令,发送者ID、发送者昵称、接受者ID、发送时间、发送内容信息
        将撒送消息送入缓存
        """
        text = self.textEdit.toPlainText()
        now_time = str(datetime.now().replace(microsecond=0))
        if text:
            self.textEdit.clear()
            self.textEdit.setFocus()
            self.textBrowser.append('<font color = green>' + self.my_info['nickname'] + f" {now_time}:" \
                                    + '<br>' + '<font color = black>' + "&nbsp;" + text)
            chat_dict = {
                'cmd': 'chat',
                'from': int(self.my_info['uid']),
                'name': self.my_info['nickname'],
                'to': int(self.frd_info['uid']),
                'time': now_time,
                'txt': text
            }
            chat_json = json.dumps(chat_dict, ensure_ascii=False)
            self.s.send(chat_json.encode())
            self.q_cache.put(chat_dict)  # 发送消息存入缓存
        else:
            QMessageBox.warning(self, "提示", "发送内容不可为空")

    def recv_msg(self, recv_dict):
        """
        接受消息：
        将接受消息及附加信息（发送者、时间）打印在聊天浏览框textBrowser
        将撒送消息送入缓存
        """
        if recv_dict['name'] == self.my_info['nickname']:
            brow_txt = '<font color = green>' + recv_dict['name'] + f" {recv_dict['time']}:<br>  " \
                       + '<font color = black>' + '&nbsp;' + recv_dict['txt']
        else:
            brow_txt = '<font color = blue>' + recv_dict['name'] + f" {recv_dict['time']}:<br>  " \
                       + '<font color = black>' + '&nbsp;' + recv_dict['txt']
        self.textBrowser.append(brow_txt)
        self.q_cache.put(recv_dict)  # 历史聊天记录，接收消息存入缓存


