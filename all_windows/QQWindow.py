# from all_ui_form.mainwindow import Ui_Mainwindow
from all_ui_form.test import Ui_Mainwindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from settingconfig import *
import json
from queue import Queue
from MyThread import *
from all_windows.ChatWindow import ChatWindow
from all_windows.AddFriend import AddFrdWindow

from all_windows.Modify import ModifyWindows
from image_handle import setlabel_imgstr


class QQWindow(QMainWindow, Ui_Mainwindow):
    '''
    主界面类：
        重要属性：
            self.frd_list_tree      dict        分组名：分组树节点
            self.frd_item_tree      dict        好友ID：好友树节点
            self.frd_info_dict      dict        好友ID：好友资料信息
            self.frd_list_dict      dict        分组名： ID列表
            self.window_dict        dict        好友ID: 聊天窗口对象
            self.queue_dict         dict        好友ID: 接收消息队列
            self.item_widget_dict   dict        好友节点画布字典
            self.add_frd_queue      Queue       接收用户查询结果队列
            self.frd_rqs_queue      Queue       接收添加好友请求队列
            self.refresh_queue      Queue       接收刷新列表消息队列
            self.recv_thread        QThread     接受服务器消息线程
            self.refresh_thread     QThread     读取刷新列表消息队列线程
        方法：
            打开修改资料视窗
            打开添加好友视窗
            服务器消息处理槽函数
            双击好友结点进入聊天视窗
            向服务器发送刷新请求
            刷新好友列表槽函数
            右键菜单显示：
                空白：
                    添加列表分组
                    刷新列表
                列表结点：
                    删除列表分组
                    修改列表分组名字
                好友结点：
                    发起聊天
                    移动分组
                    删除好友
    '''
    def __init__(self, info, sock, parent=None):
        super(QQWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("QQ")
        self.s = sock            # 套接字
        self.init_info = info    # 个人信息
        self.frd_list_tree = {}  # 分组名：分组树节点
        self.frd_item_tree = {}  # 好友ID：好友树节点
        self.frd_info_dict = {}  # ID字符串：信息
        self.frd_list_dict = {}  # 分组名： ID列表
        self.window_dict = {}    # ID: 聊天窗口对象
        self.queue_dict = {}     # ID: 接收消息队列
        self.item_widget_dict = {}  # 好友节点画布字典

        self.add_frd_queue = Queue(64)  # 接收用户查询结果队列
        self.frd_rqs_queue = Queue(128)  # 接收添加好友请求队列
        self.refresh_queue = Queue(64)  # 接收刷新好友列表请求队列

        self.add_is_show = False
        self.modify_is_show = False

        self.login_init()        # 初始化登录信息
        self.recv_thread = RecvTread(self.s)  # 创建消息接收线程
        self.recv_thread.recv_signal.connect(self.recv_handle)  # 自定义接收信号与服务器消息处理槽函数连接
        self.recv_thread.start()  # 开始线程

        self.refresh_thread = GetQueueTread(self.refresh_queue) # 创建读取刷新列表消息队列线程
        self.refresh_thread.get_signal.connect(self.refresh_friend_list)    # 自定义读取信号与刷新好友列表槽函数连接
        self.refresh_thread.start() # 开始线程

        self.treeWidget_friendlist.customContextMenuRequested.connect(self.tree_widget_showmenu)  # 右键信号连接菜单展示槽
        self.treeWidget_friendlist.doubleClicked.connect(self.click_chat)  # 节点双击连接聊天槽
        self.treeWidget_friendlist.setHeaderHidden(True)
        self.pushButton_add.clicked.connect(self.add_show)  #添加好友
        self.pushButton_modify.clicked.connect(self.modify_show)  #修改资料
        self.treeWidget_friendlist.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setCentralWidget(self.layoutWidget)
        msg_rqs_dict = {'cmd': 'offmsg', 'uid': self.init_info['uid']}
        msg_rqs_json = json.dumps(msg_rqs_dict)
        self.s.send(msg_rqs_json.encode())

    def modify_show(self):
        """
        打开修改资料视窗（如果修改资料视窗没有打开）
        """
        if not self.modify_is_show:
            self.modify_is_show = True  #关闭修改资料视窗打开使能
            self.modify_win = ModifyWindows(self.init_info,self.s,self) #创建修改资料视窗
            self.modify_win.show()

    def add_show(self):
        """
        打开添加好友视窗（如果添加好友视窗没有打开）
        """
        if not self.add_is_show:
            self.add_is_show = True #关闭添加好友视窗打开使能
            self.add_win = AddFrdWindow(self.s, self.frd_list_dict, self.add_frd_queue,
                                        self.frd_rqs_queue, self.init_info, self)   #创建添加好友视窗
            self.add_win.show()

    def recv_handle(self, msg):
        """
        服务器消息处理槽函数：
        初始化后不再由客户端掌握通信主动权,新开一RecvTread自定义线程,每当收到服务器发来的信息后该线程会发射信号。
        连接到此槽函数，在此进行判断：
                            若为消息转发，则解析发送来源，将消息送入接收消息队列,打开对应窗口后读取
                            若为查询请求，将接收到的查询结果压入接收用户查询结果队列，读取用户查询结果队列线程读取压入结果后直接作为信号发射，并连接到对应槽函数
                            若为添加好友请求，则将接收到的请求结果压入接收添加好友请求队列，读取接收添加好友请求队列线程读取压入结果后直接作为信号发射，并连接到对应槽函数
                            若为同意添加好友请求，则直接调用self.add_frd()
                            若为刷新请求，则将接收的信息压入刷新好友列表请求队列，读取刷新好友列表请求队列线程读取到压入结果后直接作为信号发射，并连接到对应槽函数
                            若为被删请求，则将接收信息中的新的好友列表信息更新本地的self.frd_list_dict，调用refresh()
        """
        recv_dict = json.loads(msg)
        if recv_dict['smd'] == 'rchat':
            frm_id = recv_dict['frm_id']
            self.queue_dict[str(frm_id)].put(recv_dict)

        elif recv_dict['smd'] == 'rsrch':
            self.add_frd_queue.put(recv_dict)

        elif recv_dict['smd'] == 'add_rqs':
            self.frd_rqs_queue.put(recv_dict)

        elif recv_dict['smd'] == 'frd_agr':
            self.add_frd(recv_dict)

        elif recv_dict['smd'] == 'refresh':
            self.refresh_queue.put(recv_dict)

        elif recv_dict['smd'] == 'rdele_frd':
            self.frd_list_dict.update(recv_dict['frd_dict'])
            self.refresh()

    def closeEvent(self, event):
        # 重写关闭事件，关闭窗口后关闭接收消息线程
        self.recv_thread.work = False
        # self.s.close()
        # TODO 关闭主窗口后上传本地缓存信息（聊天记录，分组）至数据库

    def click_chat(self):
        # 双击节点进入聊天
        click_item = self.treeWidget_friendlist.currentItem()
        if click_item.parent():
            click_id = click_item.toolTip(0)
            # 已打开的窗口不能再次打开
            if click_id not in self.window_dict.keys():
                click_info = self.frd_info_dict[click_id]
                click_info.update({'uid': click_id})
                # 创建聊天界面
                self.window_dict.update({click_id: ChatWindow(self, self.s, self.init_info, click_info, self.queue_dict[click_id])})
                self.window_dict[click_id].show()

    def refresh(self):
        """
        发送刷新请求
        """
        frd_request_dict = {
            'cmd': 'frd_rqs',
            'apd': 'refresh',
            'uid': self.init_info['uid'],
            'frd_list': self.frd_list_dict
        }
        frd_request_dict = json.dumps(frd_request_dict, ensure_ascii=False)
        self.s.send(frd_request_dict.encode())

    def refresh_friend_list(self, recv_dict):
        """
        刷新好友列表槽函数：
        更新好友ID和资料映射字典(self.frd_info_dict)
        清除整个好友列表的结点画布(self.treeWidget_friendlist)
        依据好友ID和资料映射字典重构结点画布
        """
        frd_info = recv_dict['frd_dict']
        self.frd_info_dict.update(frd_info)
        self.treeWidget_friendlist.clear()
        for list_name in self.frd_list_dict.keys():
            list_tree = QTreeWidgetItem(self.treeWidget_friendlist)
            self.frd_list_tree.update({list_name: list_tree})
            list_tree.setText(0, list_name)
            for frd_id in self.frd_list_dict[list_name]:
                frd_item = QTreeWidgetItem()
                widget = FriendItemWidget(self.frd_info_dict[str(frd_id)])
                self.item_widget_dict.update({frd_id: widget})
                frd_item.setSizeHint(0, widget.item_widget.sizeHint())
                self.frd_item_tree.update({frd_id: frd_item})
                frd_item.setToolTip(0, str(frd_id))
                list_tree.addChild(frd_item)
                self.treeWidget_friendlist.setItemWidget(frd_item, 0, widget)
                if str(frd_id) not in self.queue_dict.keys():
                    self.queue_dict.update({str(frd_id): Queue(1024)})

    def add_list(self):
        """
        添加分组：
        规范用户输入新分组名
        生成列表树节点
        更新 新分组名-列表树节点、新分组名-空ID列表到self.frd_list_tree、self.frd_list_dict
        向服务器发送更新数据表中好友列表信息请求，以及发送用户的ID和新的好友列表信息
        """
        list_name, ok = QInputDialog().getText(self, '添加分组', '请输入分组名')
        if ok:
            if list_name in self.frd_list_dict.keys():
                QMessageBox.warning(self, '提示', '分组名不能重复')
            else:
                list_tree = QTreeWidgetItem(self.treeWidget_friendlist)
                self.frd_list_tree.update({list_name: list_tree})
                self.frd_list_dict.update({list_name: []})
                list_tree.setText(0, list_name)
                up_dict = {
                    'cmd': 'up_frd_lst',
                    'uid': self.init_info['uid'],
                    'new': self.frd_list_dict
                }
                up_josn = json.dumps(up_dict, ensure_ascii=False)
                self.s.send(up_josn.encode())

    def dele_list(self):
        """
        删除分组：
        获取用户想要删除的分组和当前好友列表的第一个分组
        询问是否确定删除：
            是：
            将self.frd_list_tree中 待删除分组：待删除分组树节点 删除
            将self.frd_list_dict中 待删除分组：待删除分组下面的好友ID列表 删除
            将待删除分组下面的好友ID列表扩充到第一个分组下面的好友ID列表中
            删除画板中的待删除分组树节点
            将待删除分组下面的好友结点重构在第一个分组树节点下面
            向服务器发送更新数据表中好友列表信息请求，以及发送用户的ID和新的好友列表信息
        """
        choose_item = self.choose_item
        choose_listname=list(self.frd_list_tree.keys())[list(self.frd_list_tree.values()).index (choose_item)]  #获取用户想要删除的分组名字
        first_listname = list(self.frd_list_tree.keys())[0] if choose_listname != list(self.frd_list_tree.keys())[0] else list(self.frd_list_tree.keys())[1]    #获取当前好友列表的第一个分组名字
        message=QMessageBox.warning(self,"删除分组","是否要删除分组"+choose_listname+"，如果确定，这个分组中的好友将会被移动至" + first_listname,QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if message == QMessageBox.Yes:
            self.frd_list_tree.pop(choose_listname)
            list_IDS = self.frd_list_dict.pop(choose_listname)
            self.frd_list_dict[first_listname].extend(list_IDS)

            self.treeWidget_friendlist.takeTopLevelItem(self.treeWidget_friendlist.indexOfTopLevelItem(choose_item))

            
            for frd_id in list_IDS:
                frd_item = QTreeWidgetItem()
                widget = FriendItemWidget(self.frd_info_dict[str(frd_id)])
                self.item_widget_dict.update({frd_id: widget})
                frd_item.setSizeHint(0, widget.item_widget.sizeHint())
                self.frd_item_tree.update({frd_id: frd_item})
                frd_item.setToolTip(0, str(frd_id))
                self.frd_list_tree[first_listname].addChild(frd_item)
                self.treeWidget_friendlist.setItemWidget(frd_item, 0, widget)
                self.queue_dict.update({str(frd_id): Queue(1024)})

            up_dict = {
                'cmd': 'up_frd_lst',
                'uid': self.init_info['uid'],
                'new': self.frd_list_dict
            }
            up_josn = json.dumps(up_dict, ensure_ascii=False)
            self.s.send(up_josn.encode())

    def modi_listname(self , choose_item):
        """
        修改分组名字：
        获取用户想要删除的原分组的名字
        规范用户输入新的分组名
        直接将self.frd_list_tree、self.frd_list_dict字典中value为原分组名字替换成新分组名字
        重新设置分组结点的显示名称（新分组名）
        向服务器发送更新数据表中好友列表信息请求，以及发送用户的ID和新的好友列表信息
        """
        choose_item = self.choose_item
        list_name, ok = QInputDialog().getText(self, '修改分组名', '请输入分组名')
        #self.frd_list_tree
        raw_listname=list(self.frd_list_tree.keys())[list(self.frd_list_tree.values()).index (choose_item)]     #获取用户想要修改的原分组名字
        if ok:
            if list_name == raw_listname:
                return
            elif list_name in self.frd_list_tree.keys():
                QMessageBox.warning(self, '提示', '分组名不能重复')
            else:
                self.frd_list_tree[list_name] = self.frd_list_tree.pop(raw_listname)
                self.frd_list_dict[list_name] = self.frd_list_dict.pop(raw_listname)
                choose_item.setText(0, list_name)

                up_dict = {
                    'cmd': 'up_frd_lst',
                    'uid': self.init_info['uid'],
                    'new': self.frd_list_dict
                }
                up_josn = json.dumps(up_dict, ensure_ascii=False)
                self.s.send(up_josn.encode())

    def trans_list(self):
        """
        移动分组：
        获取想要移动好友的ID和昵称以及想要移往的新分组
        询问是否移动：
            是：
            获取所在原分组名字
            将self.frd_list_dict字典中原分组对应的ID列表中的好友ID删去并加到新分组对应ID列表中来
            画布中删除这个好友结点
            在新分组树结点下面重构好友结点和画布
            并将self.item_widget_dict、self.frd_item_tree对应项更新
            向服务器发送更新数据表中好友列表信息请求，以及发送用户的ID和新的好友列表信息
        """
        frd_uid=list(self.frd_item_tree.keys())[list(self.frd_item_tree .values()).index (self.choose_item)]
        frd_nickname=self.init_info['nickname']
        list_name = self.sender().text()    
        message=QMessageBox.question(self,"移动分组","确定要将"+frd_nickname+"移动至分组"+list_name,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if message == QMessageBox.No:
            return
        else:
            raw_listname = list(self.frd_list_tree.keys())[list(self.frd_list_tree .values()).index (self.choose_item.parent())]
            self.frd_list_dict[raw_listname].remove(frd_uid)
            self.frd_list_dict[list_name].append(frd_uid)

            self.choose_item.parent().removeChild(self.choose_item)

            frd_item = QTreeWidgetItem()
            widget = FriendItemWidget(self.frd_info_dict[str(frd_uid)])
            self.item_widget_dict.update({frd_uid: widget})
            frd_item.setSizeHint(0, widget.item_widget.sizeHint())
            self.frd_item_tree.update({frd_uid: frd_item})
            frd_item.setToolTip(0, str(frd_uid))
            self.frd_list_tree[list_name].addChild(frd_item)
            self.treeWidget_friendlist.setItemWidget(frd_item, 0, widget)

            up_dict = {
                    'cmd': 'up_frd_lst',
                    'uid': self.init_info['uid'],
                    'new': self.frd_list_dict
                }
            up_josn = json.dumps(up_dict, ensure_ascii=False)
            self.s.send(up_josn.encode())

    def dele_frd(self):
        """
        删除好友：
        获取待删除好友ID和昵称
        询问是否删除好友：
            是：
            获取待删除好友原所在分组
            将好友ID从本地self.frd_list_dict原所在分组对应的好友ID列表中删除
            删除画布中好友结点
            向服务器发送删除好友请求，用户ID、待删除好友ID以及新的分组信息
        """
        frd_uid=list(self.frd_item_tree.keys())[list(self.frd_item_tree .values()).index (self.choose_item)]    #待删除好友ID
        frd_nickname=self.frd_info_dict[str(frd_uid)]['nickname']   #待删除好友昵称
        message=QMessageBox.warning(self,"删除好友","是否要删除好友"+frd_nickname,QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if message == QMessageBox.No:
            return
        else:
            raw_listname = list(self.frd_list_tree.keys())[list(self.frd_list_tree .values()).index (self.choose_item.parent())]
            self.frd_list_dict[raw_listname].remove(frd_uid)
            self.choose_item.parent().removeChild(self.choose_item)

            up_dict = {
                    'cmd': 'dele_frd',
                    'uid': self.init_info['uid'],
                    'frd_uid': frd_uid,
                    'new': self.frd_list_dict
                }
            up_josn = json.dumps(up_dict, ensure_ascii=False)
            self.s.send(up_josn.encode())

        
    def tree_widget_showmenu(self, pos):
        """
        右键菜单显示：
            点击空白处：
                刷新列表
                添加分组
            点击列表结点：
                修改分组名字
                删除分组
            点击好友结点：
                发起聊天
                移动分组
                删除好友
        """
        self.choose_item = self.treeWidget_friendlist.itemAt(pos)
        if self.choose_item:
            parent = self.choose_item.parent()
        else:
            parent = None
        if parent is None and self.choose_item is None:
            # 空白处点击
            widget_menu = QMenu(self)
            widget_refresh = QAction('刷新', widget_menu)
            widget_refresh.triggered.connect(self.refresh)
            widget_menu.addAction(widget_refresh)   
            widget_menu.addSeparator()  #刷新列表
            widget_add = QAction('添加分组', widget_menu)
            widget_add.triggered.connect(self.add_list)
            widget_menu.addAction(widget_add)   
            widget_menu.exec_(QCursor.pos())    #添加分组

        elif parent is None:
            # 点击列表名
            list_menu = QMenu(self)
            list_rename = QAction('修改组名', list_menu)
            list_rename.triggered.connect(self.modi_listname)
            list_menu.addAction(list_rename)
            list_menu.addSeparator()    #修改组名

            list_delete = QAction('删除分组', list_menu)
            if len(self.frd_list_dict.keys()) == 1:
                list_delete.setDisabled(True)
            list_delete.triggered.connect(self.dele_list)
            list_menu.addAction(list_delete)
            list_menu.exec_(QCursor.pos())  #删除分组

        else:
            # 点击好友节点
            item_menu = QMenu(self)
            item_chat = QAction('聊天', item_menu)
            item_chat.triggered.connect(self.click_chat)
            item_menu.addAction(item_chat)
            item_menu.addSeparator()    #发起聊天
            item_cl_menu = QMenu('修改分组至', item_menu)
            item_menu.addMenu(item_cl_menu)

            list_change = []
            for list_name in self.frd_list_tree.keys():
                if self.frd_list_tree[list_name] is not parent:
                    list_change.append(QAction(list_name))
            for list_act in list_change:
                list_act.triggered.connect(self.trans_list)
                item_cl_menu.addAction(list_act)
                item_cl_menu.addSeparator()
            item_menu.addSeparator()    #修改分组

            item_delete = QAction('删除好友', item_menu)
            item_delete.triggered.connect(self.dele_frd)
            item_menu.addAction(item_delete)
            item_menu.exec_(QCursor.pos())  #删除好友



    def login_init(self):
        """
        登录初始化：
            个人资料显示（昵称、个性签名、头像）
            将本地self.frd_list_dict更新
            将服务器发送获取好友列表中全部好友资料请求，初始化标志，用户的ID以及用户的好友列表
            用获取的全部好友资料更新self.frd_info_dict
            根据好友资料信息创建画布的分组结点和好友结点显示
        """
        self.label_nickname.setText(self.init_info['nickname'])
        self.label_signature.setText(self.init_info['style_sign'])
        setlabel_imgstr(self.init_info['image'],self.label_image,100)

        frd_json = self.init_info['frd_id']
        self.frd_list_dict.update(json.loads(frd_json))     #将本地self.frd_list_dict更新
        frd_request_dict = {
            'cmd': 'frd_rqs',
            'apd': 'init',
            'uid': self.init_info['uid'],
            'frd_list': self.frd_list_dict
        }
        frd_request_json = json.dumps(frd_request_dict, ensure_ascii=False)
        self.s.send(frd_request_json.encode())
        frd_info_json = self.s.recv(BUFFSIZE * 4).decode()
        self.frd_info_dict.update(json.loads(frd_info_json))
        # 创建分组，好友节点
        for list_name in self.frd_list_dict.keys():
            list_tree = QTreeWidgetItem(self.treeWidget_friendlist)
            self.frd_list_tree.update({list_name: list_tree})
            list_tree.setText(0, list_name)
            for frd_id in self.frd_list_dict[list_name]:
                frd_item = QTreeWidgetItem()
                widget = FriendItemWidget(self.frd_info_dict[str(frd_id)])
                self.item_widget_dict.update({frd_id: widget})
                frd_item.setSizeHint(0, widget.item_widget.sizeHint())  #设置frd结点大小
                self.frd_item_tree.update({frd_id: frd_item})
                frd_item.setToolTip(0, str(frd_id))
                list_tree.addChild(frd_item)

                self.treeWidget_friendlist.setItemWidget(frd_item, 0, widget)
                self.queue_dict.update({str(frd_id): Queue(1024)})

    def add_frd(self, recv_dict):
        """
        添加新好友结点到画布
        先获取选择添加的分组和新好友ID
        如果选择添加的分组被删除了，则直接放入当前第一个分组
        在选择分组树节点下面构建新好友结点
        """
        grp = recv_dict['grp']
        frd_id = recv_dict['frd_id']
        if grp not in self.frd_list_dict.keys():
            for grp_name in self.frd_list_dict.keys():
                grp = grp_name
                break
        self.frd_list_dict[grp].append(frd_id)
        self.queue_dict.update({str(frd_id): Queue(1024)})
        self.frd_info_dict.update({str(frd_id): recv_dict['frd_info']})
        frd_item = QTreeWidgetItem()
        widget = FriendItemWidget(self.frd_info_dict[str(frd_id)])
        self.item_widget_dict.update({frd_id: widget})
        frd_item.setSizeHint(0, widget.item_widget.sizeHint())
        self.frd_item_tree.update({frd_id: frd_item})
        frd_item.setToolTip(0, str(frd_id))
        self.frd_list_tree[grp].addChild(frd_item)
        self.treeWidget_friendlist.setItemWidget(frd_item, 0, widget)


class FriendItemWidget(QWidget):
    """
    好友结点画布类：
        控件：
            头像label
            昵称label
            在线状态label
            个性签名label
        布局：
            ****************************
            *    头  昵称  在线状态     *
            *    像     个性签名        *
            ****************************
        设置控件显示
    """
    def __init__(self, frd_info):
        super().__init__()
        self.item_widget = QWidget(self)
        self.img_lb = QLabel()
        self.nk_lb = QLabel(frd_info['nickname'])
        self.stat_lb = QLabel({'on': '在线', 'off': '离线'}[frd_info['status']])
        self.sign_lb = QLabel(frd_info['style_sign'])

        setlabel_imgstr(frd_info['image'],self.img_lb,60)

        self.main_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.h_layout.addWidget(self.nk_lb)
        self.h_layout.addWidget(self.stat_lb)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.sign_lb)
        self.main_layout.addWidget(self.img_lb)
        self.main_layout.addLayout(self.v_layout)
        self.item_widget.setLayout(self.main_layout)





