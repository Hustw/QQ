import numpy as np
import cv2
from base64 import b64encode,b64decode
import os
from PyQt5.QtGui import *

def imgpath2imgstr(path):
    """
    将输入的图片路径转化为数据库支持的图片字符串格式
    """
    img=cv2.imread(path)
    (_,extension) = os.path.splitext(path)
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]
    result, imgencode = cv2.imencode(extension, img, encode_param)
    data = np.array(imgencode)
    stringData = b64encode(data.tostring())
    imgstr = stringData.decode('utf-8')
    return imgstr

def cvimg_to_qtimg(cvimg):
    """
    将OpenCV读取的二进制数据流格式转化为Qtimg格式
    """
    height, width, depth = cvimg.shape
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
    return cvimg

def imgstr2imgQt(imgstr):
    """
    将数据库支持的图片字符串格式转化为Qtimg格式
    """
    img_B64code = imgstr.encode('utf-8')
    img_string= b64decode(img_B64code)
    data = np.frombuffer(img_string, np.uint8)#将获取到的字符流数据转换成1维数组
    img_cv =cv2.imdecode(data,cv2.IMREAD_COLOR)#将数组解码成图像
    img_Qt =cvimg_to_qtimg(img_cv)
    return img_Qt

def setlabel_imgstr(imgstr,label,size):
    """
    将数据库支持的图片字符串对应的图片在label上显示
    """
    img_Qt = imgstr2imgQt(imgstr)
    pix = QPixmap(img_Qt)
    label.resize(size,size)
    label.setPixmap(pix)
    label.setMaximumSize(size, size)
    label.setScaledContents(True)

def setlabel_imgpath(imgpath,label,size):
    """
    将路径对应的图片在label上显示
    """
    pix = QPixmap(imgpath)
    label.resize(size,size)
    label.setPixmap(pix)
    label.setMaximumSize(size, size)
    label.setScaledContents(True)
