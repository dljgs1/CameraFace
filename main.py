#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import PyQt5.QtGui as QtGui

import cv2

class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI() #界面绘制交给InitUi方法
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.TimerOutFun)
        self.timer_camera.start()
        self.timer_camera.setInterval(1)
        self.camera = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
    def TimerOutFun(self):
        success, img = self.camera.read()
        if success :
            self.image = img
            self.ShowImage()

    def ShowImage(self):
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        if self.image.ndim == 3:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.image #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

        faces = self.face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
        result = []
        for (x,y,width,height) in faces:
            cv2.rectangle(show, (x,y), (x+width, y+height), (0, 0, 255)) 
            # result.append((x,y,x+width,y+height))
        
        qimg = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.DispLb.setPixmap(QtGui.QPixmap.fromImage(qimg).scaled(self.DispLb.width(), self.DispLb.height()))
        self.DispLb.show()

    def ChangeMinArgValue(self, value):
        print(value)
    
    def ChangeMaxArgValue(self, value):
        print(value)
    

    def initUI(self):
        #设置窗口的位置和大小
        self.setGeometry(300, 300, 800, 600)  
        #设置窗口的标题
        self.setWindowTitle('摄像头人脸捕获工具')
        #设置窗口的图标，引用当前目录下的web.png图片
        self.setWindowIcon(QIcon('web.png'))        
        #摄像头窗口
        self.DispLb = QLabel('Zetcode', self)
        self.DispLb.move(0, 0)
        self.DispLb.setFixedSize(600, 450)
        # 
        self.sldmin = QSlider(Qt.Horizontal, self)
        self.sldmax = QSlider(Qt.Horizontal, self)
        self.sldmin.setGeometry(10, 480, 100, 30)
        self.sldmax.setGeometry(10, 520, 100, 30)
        self.sldmin.valueChanged[int].connect(self.ChangeMinArgValue)
        self.sldmax.valueChanged[int].connect(self.ChangeMaxArgValue)

        # button
        self.btnSave = QPushButton('保存头像', self)
        self.btnSave.setCheckable(True)
        self.btnSave.move(100, 480)
        self.btnSave2 = QPushButton('设置模式', self)
        self.btnSave2.setCheckable(True)
        self.btnSave2.move(300, 480)

        #显示窗口
        self.show()
        
        
if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_()) 