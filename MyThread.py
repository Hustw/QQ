from PyQt5.QtCore import *
from settingconfig import *


class RecvTread(QThread):
    """
    接收消息线程类：
        继承 QTread 类,自定义发射信号 recv_signal 并重写 run 函数
        当self.work为 True 即主窗口未关闭时，循环、阻塞地接收来自服务器的消息字符串并作为信号发射
    """
    recv_signal = pyqtSignal(str)

    def __init__(self, sock, parent=None):
        super(RecvTread, self).__init__(parent)
        self.s = sock
        self.work = True

    def run(self):
        while self.work:
            recv_msg = self.s.recv(BUFFSIZE * 4).decode()
            # TODO 全局标志，handle处理完信息后再发射？
            self.recv_signal.emit(recv_msg)


class GetQueueTread(QThread):
    """
    读取消息队列线程类：
        继承 QTread 类，自定义发射信号 get_signal 并重写 run 函数
        当self.working为 True 即聊天窗口未关闭时，循环、阻塞地从该好友的消息队列中读取消息字典并作为信号发射
    """
    get_signal = pyqtSignal(dict)

    def __init__(self, q, parent=None):
        super(GetQueueTread, self).__init__(parent)
        self.q = q
        self.working = True

    def run(self):
        while self.working:
            self.get_signal.emit(self.q.get())
