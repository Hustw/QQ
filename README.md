# 私人聊天QQ

开发人员：吴雨暄，吴栋

## 项目简介

基于Python，PyQt5开发一个私人即时聊天软件

本项目现放在https://github.com/Hustw/QQ, 后续可能会时不时地进行维护

## Installation

​	1.安装依赖包

```
pip install -r requirements.txt
```

​	2.MySQL数据库下载安装教程

```
参考教程： https://blog.csdn.net/zhouzezhou/article/details/52446608

下载时间过长可换用迅雷下载
```

## Initial

​	1.启动数据库

```
Windows下： net start Name
Name是配置mysql server时填写的服务器名称
```

​	2.修改 dbsql.py 中

```
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
```

​	中的password为自己设置的MySQL密码

​	3.运行 dbsql.py

## Start

​	1.运行 server.py

​	2.运行 QQlogin.py

​	注：首次运行需先注册

## 基本功能

​	注册

​	登录

​	添加好友

​	聊天

​	联系人管理

​	修改个人资料