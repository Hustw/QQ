from PyQt5.QtWidgets import *
import json
from all_ui_form.addfrd import Ui_AddFrd
from MyThread import *
from image_handle import *


class AddFrdWindow(QMainWindow, Ui_AddFrd):
    """
    添加好友界面类：
        重要属性：
            self.item_widget_dict       查找好友列表项画布字典
            self.rqs_item_widget_dict   好友请求列表画布字典
            self.recv_thread            查找反馈消息读取进程
            self.rqs_thread             添加好友请求消息读取进程
        主要方法：
            查询函数
            展示查询函数
            展示请求函数
    """
    def __init__(self, sock, group, q, rqs_q, my_info, main_win, parent=None):
        super(AddFrdWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("添加好友")
        self.s = sock
        self.q = q
        self.rqs_q = rqs_q
        self.my_info = my_info
        self.group_name = group.keys()
        self.group_list = group
        self.main_win = main_win
        self.srch_lst_itm = []
        self.rqst_lst_itm = []

        self.item_widget_dict = {}  # 查找好友列表项画布字典
        self.rqs_item_widget_dict = {}  # 好友请求列表画布字典

        self.recv_thread = GetQueueTread(self.q)  # 查找反馈消息读取进程
        self.rqs_thread = GetQueueTread(self.rqs_q)  # 添加好友请求消息读取进程
        self.recv_thread.get_signal.connect(self.show_search)   # 自定义队列读取信号连接展示读取消息槽函数
        self.rqs_thread.get_signal.connect(self.show_request)   # 自定义队列读取信号连接展示读取消息槽函数
        self.recv_thread.start()
        self.rqs_thread.start()
        self.pushButton_search.setShortcut('return')
        self.pushButton_search.clicked.connect(self.search)
        self.lineEdit_index.setFocus()

    def closeEvent(self, event):
        """
        结束队列读取进程
        """
        self.recv_thread.working = False
        self.rqs_thread.working = False
        self.q.put({'smd': '', 'srchlst': []})  #给队列喂一个无用数据促使进程退出
        self.rqs_q.put({'smd': '', 'frm_id': '', 'nick': '', 'image': ''})   #给队列喂一个无用数据促使进程退出
        self.main_win.add_is_show = False
        self.close()


    def search(self):
        """
        查询函数：
            向服务器发送查询新好友请求和查询索引(昵称 or ID)
        """
        index = self.lineEdit_index.text()
        if index:
            search_dict = {
                'cmd': 'srch',
                'index': index
            }
            search_json = json.dumps(search_dict, ensure_ascii=False)
            self.s.send(search_json.encode())

    def show_search(self, recv_dict):
        """
        展示查询函数：
            清除查询结果画布显示
            根据服务器返回的查询结果重构添加结点画布显示
        """
        self.listWidget_search.clear()
        if not recv_dict['srchlst']:
            item = QListWidgetItem(self.listWidget_search)
            item.setText('未找到符合要求的联系人')
            return
        for user_dict in recv_dict['srchlst']:
            widget = AddItemWidget(self.s, user_dict, self.group_name, self.my_info, self.group_list)
            self.item_widget_dict.update({widget.id_lb.text(): widget})
            item = QListWidgetItem(self.listWidget_search)
            item.setSizeHint(widget.item_widget.sizeHint())
            self.listWidget_search.addItem(item)
            self.listWidget_search.setItemWidget(item, widget.item_widget)
            self.srch_lst_itm.append(item)

    def show_request(self, recv_dict):
        """
        展示请求函数：
            添加新的请求结点到画布显示
        """
        widget = RequestItemWidget(recv_dict, self.group_name, self.s, self.my_info,self.main_win)
        self.rqs_item_widget_dict.update({recv_dict['frm_id']: widget})
        item = QListWidgetItem(self.listWidget_rqst)
        item.setSizeHint(widget.item_widget.sizeHint())
        self.listWidget_rqst.addItem(item)
        self.listWidget_rqst.setItemWidget(item, widget.item_widget)
        self.rqst_lst_itm.append(widget)

class AddItemWidget(QWidget):
    """
    添加结点画布：
        控件：
            头像label
            IDlabel
            昵称label
            添加按钮
            选择分组下拉框
        方法：
            添加好友
    """
    def __init__(self, sock, user_dict, group_name, my_info, frd_list):
        super().__init__()
        self.s = sock
        self.my_info = my_info
        self.item_widget = QWidget(self)
        self.add_btn = QPushButton('添加')
        # 已经添加不可重复添加
        for grp in group_name:
            if user_dict['uid'] in frd_list[grp] or user_dict['uid'] == my_info['uid']:
                self.add_btn.setText('已添加')
                self.add_btn.setDisabled(True)
                break   
        self.id_lb = QLabel(str(user_dict['uid']))
        self.img_lb = QLabel()
        setlabel_imgstr(user_dict['image'],self.img_lb,60)
        self.nick_lb = QLabel(user_dict['nickname'])
        self.grb_box = QComboBox(self.item_widget)
        self.grb_box.addItems([grp for grp in group_name])

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.img_lb)
        self.h_layout.addWidget(self.id_lb)
        self.h_layout.addWidget(self.nick_lb)
        self.h_layout.addWidget(self.add_btn)
        self.h_layout.addWidget(self.grb_box)

        self.item_widget.setLayout(self.h_layout)
        self.add_btn.clicked.connect(self.add)

    def add(self):
        """
        添加好友：
        向服务器发送添加好友请求、用户ID、用户昵称、待添加好友ID、选择分组信息
        """
        add_dict = {
            'cmd': 'add',
            'my_id': self.my_info['uid'],
            'image': self.my_info['image'],
            'nick': self.my_info['nickname'],
            'to_id': int(self.id_lb.text()),
            'grp': self.grb_box.currentText()
        }
        add_json = json.dumps(add_dict, ensure_ascii=False)
        self.s.send(add_json.encode())
        QMessageBox.information(self, '提示', '好友申请已经发送\n等待对方审核通过')


class RequestItemWidget(QWidget):
    """
    请求结点画布类：
        控件：
            头像label
            IDlabel
            昵称label
            同意按钮
            拒绝按钮
        方法：
            同意添加
            拒绝添加
    """
    def __init__(self, user_dict, group_name, sock, my_info, main_win):
        super().__init__()
        self.main_win = main_win
        self.group_name = group_name
        self.s = sock
        self.my_info = my_info
        self.user_dict = user_dict
        self.item_widget = QWidget(self)
        self.agree_btn = QPushButton('同意')
        self.rejct_btn = QPushButton('拒绝')
        self.id_lb = QLabel(self.user_dict['frm_id'])
        self.nick_lb = QLabel(self.user_dict['nick'])
        self.img_lb = QLabel()
        if self.user_dict['image']:
            setlabel_imgstr(self.user_dict['image'],self.img_lb,60)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.img_lb)
        self.h_layout.addWidget(self.id_lb)
        self.h_layout.addWidget(self.nick_lb)
        self.h_layout.addWidget(self.agree_btn)
        self.h_layout.addWidget(self.rejct_btn) #水平布局

        self.item_widget.setLayout(self.h_layout)
        self.agree_btn.clicked.connect(self.agree)
        self.rejct_btn.clicked.connect(self.rejct)

    def agree(self):
        """
        同意添加：
            选择添加分组
            向服务器发送同意添加指令、好友ID、用户ID、用户选择分组、好友选择分组
        """
        if self.id_lb.text() in self.main_win.frd_info_dict.keys():
            QMessageBox.warning(self, '提示', '好友已添加，请勿重复添加！')
            return
        gname, ok = QInputDialog.getItem(self, '提示信息', '请选择分组', self.group_name)
        if ok:
            agree_dict = {
                'cmd': 'agr_frd',
                'frd_id': int(self.id_lb.text()),
                'my_id': self.my_info['uid'],
                'my_grp': gname,
                'frd_grp': self.user_dict['grp']
            }
            agree_json = json.dumps(agree_dict, ensure_ascii=False)
            self.s.send(agree_json.encode())

    def rejct(self):
        # 拒绝添加
        pass


