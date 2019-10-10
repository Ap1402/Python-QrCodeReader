import interfaz as i
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from random import randint
import threading
import time

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

class Interfaz(i.Ui_MainWindow):
    def startUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.image=None
        self.iniciarButton.clicked.connect(self.startWebcam)
        self.detenerButton.clicked.connect(self.stopWebcam)

    def startWebcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(3,301)
        self.capture.set(4,211)
        
        self.timer= QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret,self.image=self.capture.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image=cv2.flip(self.image,1)

        self.decodedObjects = self.decode(self.image)

        self.displayImage(self.image,1)

    def stopWebcam(self):
        self.timer.stop()
    
    def displayImage(self,img,window=1):
        qformat=QtGui.QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QtGui.QImage.Format_RGBA8888
            else:
                qformat=QtGui.QImage.Format_RGB888

        outImage=QtGui.QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage= outImage.rgbSwapped()

        if window==1:
            self.video.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.video.setScaledContents(True)

    def decode(self,im) : 
        self.decodedObjects = pyzbar.decode(im)
        for obj in self.decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data,'\n')     
        return self.decodedObjects


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Interfaz()
ui.startUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())