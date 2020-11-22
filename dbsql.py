import pymysql
import settingconfig
import json


class DataBase(object):
    """
    数据库类：
        初始化连接到MySQL数据库并建立游标
        方法：
            create_table(self) 建立一个user表
            insert_user(self, ...) 向表中插入一行数据
            select_user(self, ...) 查找符合条件的数据
            delete_user(self, ...) 删除一行数据
            cls_cnt(self) 关闭游标和连接

    """
    def __init__(self):
        # 连接本地数据库
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            database="qqusers",
            charset="utf8")
        self.cursor = self.conn.cursor()
        print('connect ok')

    def cls_cnt(self):
        """
        关闭游标，链接
        """
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        """
        创建用户数据表
        """
        cmd = """CREATE TABLE users (
                 uid int auto_increment primary key,
				 image text,
                 nickname varchar(32),
                 password varchar(32),
                 gender enum('男','女','保密'),
                 region_prov varchar(32),
                 region_city varchar(32),
                 birthday varchar(32),
                 style_sign tinytext,
                 frd_id tinytext,
                 status enum('on','off'));
              """
        self.cursor.execute(cmd)
        cmd = """
                ALTER TABLE users AUTO_INCREMENT=100001;
              """
        self.cursor.execute(cmd)

    def insert_user(self, image, nickname, password, gender, region_prov, region_city, birthday, style_sign):
        """
        用户注册--插入用户资料，返回生成的自增ID
        """
        frd_dict = {'我的好友': []}
        frd_json = json.dumps(frd_dict, ensure_ascii=False)

        cmd = '''INSERT INTO users(image, nickname, password, gender, region_prov, region_city, birthday, style_sign, frd_id, status)
                values("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", '{}', "{}")'''.format \
                (image, nickname, password, gender, region_prov, region_city, birthday, style_sign, frd_json, 'off')
        self.cursor.execute(cmd)
        self.conn.commit()
        cmd = """
                SELECT LAST_INSERT_ID(); 
              """
        self.cursor.execute(cmd)
        data = self.cursor.fetchone()
        return data[0]

    def delete_user(self, uid):
        """
        删除用户--删除用户资料
        """
        cmd = """DELETE FROM users where uid='%s'""" % uid
        self.cursor.execute(cmd)
        self.conn.commit()

    def select_user(self, tid, pwd):
        """
        用户登录 -- 查询自身信息
        """
        cmd = """SELECT uid,image,nickname,password,gender,region_prov,region_city,birthday,style_sign,frd_id FROM users where 
                 uid=%d and password='%s'""" % (int(tid), pwd)
        self.cursor.execute(cmd)
        data = self.cursor.fetchall()
        return data

    def select_frd(self, uid, frd_list):
        """
        登录初始化/更新好友信息--获取用户的好友列表中所有好友的信息
        """
        frd_info = {}
        for list_name in frd_list.keys():
            for frd_id in frd_list[list_name]:
                cmd = """SELECT image,nickname,gender,region_prov,region_city,birthday,style_sign,status FROM users where
                         uid=%d""" % frd_id
                self.cursor.execute(cmd)
                info = self.cursor.fetchone()
                info_dict = dict(zip(('image','nickname', 'gender', 'region_prov',
                                      'region_city', 'birthday', 'style_sign', 'status'), info))  ###
                frd_info.update({frd_id: info_dict})
        return frd_info

    def update_frd(self, uid, grp, new_id):
        """
        添加好友--更新用户的好友列表信息（将新好友添加到选择的分组）
        """
        cmd = """SELECT frd_id FROM users where uid=%d""" % uid
        self.cursor.execute(cmd)
        frd_id_json = self.cursor.fetchone()
        frd_id_dict = json.loads(frd_id_json[0])
        frd_id_dict[grp].append(new_id)
        new_json = json.dumps(frd_id_dict, ensure_ascii=False)
        cmd = """UPDATE users SET frd_id='%s' where uid = %d""" % (new_json, uid)
        self.cursor.execute(cmd)
        self.conn.commit()

    def select_frd_frd_id(self, frd_id):
        """
        查询好友的好友列表的信息
        """
        cmd = """SELECT frd_id,status FROM users where uid=%d""" % frd_id
        self.cursor.execute(cmd)
        info = self.cursor.fetchone()
        return info

    def update_frd_lst(self, uid, frd_lst):
        """
        更新用户的好友列表信息
        """
        frd_json = json.dumps(frd_lst, ensure_ascii=False)
        cmd = """UPDATE users SET frd_id='%s' where uid=%d""" % (frd_json, uid)
        self.cursor.execute(cmd)
        self.conn.commit()

    def update_online_status(self, uid, status):
        """
        更新用户的在线状态信息
        """
        cmd = """UPDATE users SET status='%s' where uid=%d""" % (status, uid)
        self.cursor.execute(cmd)
        self.conn.commit()

    def search_user(self, index):
        """
        添加搜索好友--根据ID或昵称查询用户信息
        """
        int_index = 0
        if index.isdecimal():
            int_index = int(index)
        cmd = """SELECT uid,image,nickname,gender,region_prov,region_city,birthday,style_sign from users 
                 where uid = %d or nickname = '%s'""" % (int_index, index)
        self.cursor.execute(cmd)
        info = self.cursor.fetchall()
        return info

    def select_all_uid(self):
        """
        获取表中所有用户的ID
        """
        cmd = """SELECT uid from users"""
        self.cursor.execute(cmd)
        all_uid = self.cursor.fetchall()
        return all_uid

    def find_with_id(self, uid):
        """
        同意添加好友--根据ID获取用户公开信息
        """
        cmd = """SELECT image,nickname,gender,region_prov,region_city,birthday,style_sign,status from users 
                 where uid = %d""" % uid
        self.cursor.execute(cmd)
        info = self.cursor.fetchone()
        return info
    
    def update_all(self,msg):
        """
        更新用户的所有信息
        """
        cmd = """UPDATE users SET image = '%s', nickname = '%s', password = '%s', gender = '%s', region_prov = '%s', region_city = '%s', birthday = '%s', style_sign = '%s' where uid=%d""" % (msg['img'],
        msg['nknm'],msg['pswd'],msg['gd'],msg['prv'],msg['cty'],msg['bir'],msg['sty'],msg['uid'])
        self.cursor.execute(cmd)
        self.conn.commit()

if __name__ == '__main__':

    db = DataBase()
    db.create_table()
    db.cls_cnt()


