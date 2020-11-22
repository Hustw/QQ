from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Ui_Mainwindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(585, 688)
        self.label_image = QLabel()
        self.layoutWidget = QWidget(Form)
        self.treeWidget_friendlist = QTreeWidget()
        self.pushButton_add = QPushButton()
        self.pushButton_modify = QPushButton()
        self.pushButton_files = QPushButton()
        self.label_nickname = QLabel()
        self.label_signature = QLabel()
        self.pushButton_add.setText('添加好友')
        self.pushButton_modify.setText("修改资料")
        self.main_layout = QVBoxLayout()
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.label_nickname)
        self.v_layout.addWidget(self.label_signature)
        self.h1_layout.addWidget(self.label_image)
        self.h1_layout.addLayout(self.v_layout)
        self.main_layout.addLayout(self.h1_layout)
        self.main_layout.addWidget(self.treeWidget_friendlist)
        self.h2_layout.addWidget(self.pushButton_add)
        self.h2_layout.addWidget(self.pushButton_files)
        self.h2_layout.addWidget(self.pushButton_modify)
        self.main_layout.addLayout(self.h2_layout)

        self.layoutWidget.setLayout(self.main_layout)

