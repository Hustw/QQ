import socket
from settingconfig import *
import select
from dbsql import DataBase
import json
import datetime
from queue import Queue
from time import sleep
input_list = []


class Server(object):
    r"""
    服务器类：
        初始化：建立套接字并绑定IP和端口
        方法：
            run_server(self)：
                采用select()方法监听返回触发的文件描述符，若是服务器端触发则有新连接请求
                若是其他套接字触发则调用event_handle时间处理函数
            event_handle:
                识别客户端请求类型并做响应处理
    """
    def __init__(self):
        self.s = socket.socket()
        self.host = HOST
        self.port = PORT
        self.on_line_list = {}
        self.msg_queue_dict = {}
        input_list.append(self.s)
        self.s.bind((self.host, self.port))
        self.s.listen(10)
        self.init_queue()
        self.run_server()

    def init_queue(self):
        """
        """
        db = DataBase()
        all_uid = db.select_all_uid()
        db.cls_cnt()
        for uid in all_uid:
            self.msg_queue_dict.update({uid[0]: Queue(1024)})

    def run_server(self):
        """
        启动监听，判别触发源
        如果是服务器触发，添加新的客户端连接
        如果是客户端触发，调用客户端事件处理函数
        """
        while True:
            print('waiting for selecting...')
            rlist, wlist, xlist = select.select(input_list, [], input_list)
            for r in rlist:
                if r == self.s:
                    con, addr = self.s.accept()
                    con.send("ok".encode())
                    input_list.append(con)
                else:
                    self.event_handle(r)

    def event_handle(self, con):
        """
        客户端事件处理函数
        """
        try:
            msg = con.recv(BUFFSIZE).decode()
            msg = json.loads(msg)

            if msg['cmd'] == 'log':  # 登录
                """
                用户登录:查表返回用户的全部个人信息，并更新用户的在线状态为在线
                """
                uid = msg['uid']
                pwd = msg['pwd']
                if int(uid) in self.on_line_list.keys():
                    con.send("Online".encode())
                    return
                db = DataBase()
                data = db.select_user(uid, pwd)     #查询用户的全部信息
                if len(data):
                    dict_data = dict(zip(('uid', 'image','nickname', 'password', 'gender', 'region_prov', 'region_city',
                                          'birthday', 'style_sign', 'frd_id'), data[0]))
                    jdata = json.dumps(dict_data, ensure_ascii=False)
                    con.send("True".encode())
                    con.send(jdata.encode())    #用户信息回传
                    self.on_line_list.update({dict_data['uid']: con})   #更改用户的在线状态
                    db.update_online_status(dict_data['uid'], 'on')
                else:
                    con.send("False".encode())
                db.cls_cnt()
            elif msg['cmd'] == 'offmsg':
                uid = msg['uid']
                while not self.msg_queue_dict[uid].empty():
                    offmsg = self.msg_queue_dict[uid].get()
                    con.send(offmsg.encode())
                    sleep(0.02)
            elif msg['cmd'] == 'reg':  # 注册
                """
                新用户注册:将新用户的信息插入数据表，并返回生成的ID
                """
                db = DataBase()
                id = db.insert_user(msg['img'],msg['nknm'], msg['pswd'], msg['gd'],
                               msg['prv'], msg['cty'], msg['bir'], msg['sty'])
                con.send(str(id).encode())  #返回生成的ID
                db.cls_cnt()
            elif msg['cmd'] == 'frd_rqs':  # 登录初始化/更新好友信息
                """
                登录初始化:向客户端发送用户的好友列表中所有好友的信息
                更新好友信息:向客户端发送更新指令和用户的好友列表中所有好友的信息
                """
                db = DataBase()
                frd_info = db.select_frd(msg['uid'], msg['frd_list'])   #获取用户的好友列表中所有好友的信息
                if msg['apd'] == 'init':
                    frd_json = json.dumps(frd_info, ensure_ascii=False)
                    con.send(frd_json.encode())
                elif msg['apd'] == 'refresh':
                    send_dict = {
                        'smd': 'refresh',
                        'frd_dict': frd_info
                    }
                    send_json = json.dumps(send_dict, ensure_ascii=False)
                    con.send(send_json.encode())
                db.cls_cnt()

            elif msg['cmd'] == 'chat':  # 聊天信息转发
                """
                聊天记录转发:
                若接收客户端在线，直接将聊天信息（聊天指令、发送者id、发送者昵称、发送时间、发送内容）转发过去
                若接受客户端不在线，暂时将待转化内容压入self.msg_queue_dict
                """
                from_id = msg['from']
                from_name = msg['name']
                to_id = msg['to']
                time = msg['time']
                text = msg['txt']
                send_dict = {
                    'smd': 'rchat',
                    'frm_id': from_id,
                    'name': from_name,
                    'time': time,
                    'txt': text
                }
                send_json = json.dumps(send_dict, ensure_ascii=False)
                if to_id in self.on_line_list.keys():
                    to_con = self.on_line_list[to_id]
                    to_con.send(send_json.encode())
                else:
                    self.msg_queue_dict[to_id].put(send_json)

            elif msg['cmd'] == 'srch':  # 查找联系人
                """
                查找联系人：将基于ID或昵称的查询到的所有用户的信息回传，并回传刷新搜索结果栏指令
                """
                db = DataBase()
                search_info = db.search_user(msg['index'])
                db.cls_cnt()
                info_list = []
                for info in search_info:
                    info_dict = dict(zip(('uid', 'image', 'nickname', 'gender', 'region_prov', 'region_city',
                                          'birthday', 'style_sign'), info))
                    info_list.append(info_dict)
                send_dict = {
                    'smd': 'rsrch',
                    'srchlst': info_list
                }
                send_json = json.dumps(send_dict, ensure_ascii=False)
                con.send(send_json.encode())

            elif msg['cmd'] == 'add':  # 添加好友请求
                """
                添加好友请求：
                若接受客户端在线，直接将请求用户的id信息、昵称信息、选择添加分组信息（暂存）、添加好友请求指令发送过去
                若接受客户端不在线，暂时将待转化内容压入self.msg_queue_dict
                """
                to_id = msg['to_id']
                frm_id = msg['my_id']
                frm_nick = msg['nick']
                send_dict = {
                    'smd': 'add_rqs',
                    'frm_id': str(frm_id),
                    'image': msg['image'],
                    'nick': frm_nick,
                    'grp': msg['grp']
                }
                send_json = json.dumps(send_dict, ensure_ascii=False)
                if to_id in self.on_line_list.keys():
                    to_con = self.on_line_list[to_id]
                    to_con.send(send_json.encode())
                else:
                    self.msg_queue_dict[to_id].put(send_json)

            elif msg['cmd'] == 'agr_frd':  # 同意添加好友请求
                """
                同意添加好友请求：
                同意方当前一定在线，直接将请求方的公开信息，同意方选择的分组信息，以及同意添加指令发送给同意方
                若请求方当前在线，直接将同意方的公开信息，请求方选择的分组信息，以及同意添加指令发送给请求方
                若请求方不在线，暂时将待转化内容压入self.msg_queue_dict
                """
                frd_id = msg['frd_id']
                my_id = msg['my_id']
                frd_grp = msg['frd_grp']
                my_grp = msg['my_grp']
                db = DataBase()
                frd_info = db.find_with_id(frd_id)
                my_info = db.find_with_id(my_id)
                db.update_frd(my_id, my_grp, frd_id)
                db.update_frd(frd_id, frd_grp, my_id)
                db.cls_cnt()
                frd_info_dict = dict(zip(('image', 'nickname', 'gender', 'region_prov', 'region_city',
                                          'birthday', 'style_sign', 'status'), frd_info))
                send2me_dict = {
                    'smd': 'frd_agr',
                    'frd_info': frd_info_dict,
                    'frd_id': frd_id,
                    'grp': msg['my_grp']
                }
                my_con = self.on_line_list[my_id]
                send2me_json = json.dumps(send2me_dict, ensure_ascii=False)
                my_con.send(send2me_json.encode())
                my_info_dict = dict(zip(('image', 'nickname', 'gender', 'region_prov', 'region_city',
                                         'birthday', 'style_sign', 'status'), my_info))
                send2frd_dict = {
                    'smd': 'frd_agr',
                    'frd_info': my_info_dict,
                    'frd_id': my_id,
                    'grp': msg['frd_grp']
                }
                send2frd_json = json.dumps(send2frd_dict, ensure_ascii=False)
                if frd_id in self.on_line_list.keys():
                    frd_con = self.on_line_list[frd_id]
                    frd_con.send(send2frd_json.encode())
                else:
                    self.msg_queue_dict[frd_id].put(send2frd_json)
                # TODO 可以不单独设计命令，而是和刷新列表命令复用，即服务器发出一个刷新两用户列表的指令

            elif msg['cmd'] == 'up_frd_lst':
                """
                更新数据表中用户的好友列表信息
                """
                db = DataBase()
                db.update_frd_lst(msg['uid'], msg['new'])
                db.cls_cnt()

            elif msg['cmd'] == 'dele_frd':
                """
                删除好友：
                请求方当前一定在线，直接将数据表中请求方的好友列表更新（删除被删方）
                若被删方当前不在线，直接将数据表中被删方的好友列表更新（删除请求方）
                若被删方当前在线，向被删方发送被删指令，传送更新后的好友列表（删除请求方），控制待删方更新本地列表信息，并自动调用刷新列表操作
                """
                db = DataBase()
                db.update_frd_lst(msg['uid'], msg['new'])
                info=db.select_frd_frd_id(msg['frd_uid'])
                info_dict = dict(zip(('frd_id','status'), info))
                frd_json = info_dict['frd_id']
                #把数据表中待删除好友的好友列表信息更新(互删)
                frd_list_dict={}
                frd_list_dict.update(json.loads(frd_json))
                for listname , id_list in frd_list_dict.items():
                    if msg['uid'] in id_list:
                        frd_list_dict[listname].remove(msg['uid'])
                #待删方不在线，直接修改数据表
                if info_dict['status'] == 'off':
                    db.update_frd_lst(msg['frd_uid'],frd_list_dict)
                #在线向待删方客户端发起通知，传送修改后的好友列表，待删除好友本地更新列表信息后，自动刷新
                else:
                    to_con = self.on_line_list[msg['frd_uid']]
                    send_dict = {
                        'smd': 'rdele_frd',
                        'frd_dict': frd_list_dict
                    }
                    send_json = json.dumps(send_dict, ensure_ascii=False)
                    to_con.send(send_json.encode())
                db.cls_cnt()

            elif msg['cmd'] == 'modify':
                """
                修改资料：更新数据表中全部个人信息
                """
                db = DataBase()
                message=db.update_all(msg)
                db.cls_cnt()
                


        except Exception as e:
            print(e)
            input_list.remove(con)
            del_id = None
            for the_id in self.on_line_list.keys():
                if self.on_line_list[the_id] is con:
                    del_id = the_id
                    break
            if del_id:
                db = DataBase()
                db.update_online_status(del_id, 'off')
                db.cls_cnt()
                del self.on_line_list[del_id]
            return


if __name__ == '__main__':
    server = Server()