from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from commands import command
import time

class remoteDisplay(QWidget):
    def __init__(self, mainObject):
        super().__init__()
        self.mainObject = mainObject
        self.resize(1600, 900)
        self.setMouseTracking(True)
        self.vbox = QVBoxLayout()
        self.label = QLabel()
        self.label.setMouseTracking(True)
        self.vbox.addWidget(self.label)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setLayout(self.vbox)
        self.someevent = {}
        self.keyboardevent = {}
        self.scrollevent = {}

    def updatetheframe(self, pixmap):
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.mainObject.remoteWindowclosed = True
    
    def mouseMoveEvent(self,  event):
        self.sendMouseEvent(event)
    
    def mousePressEvent(self,  event):
        self.sendMouseEvent(event)
    
    def mouseReleaseEvent(self,  event):
        self.sendMouseEvent(event)
    
    def keyPressEvent(self, event):
        self.sendKeyEvent(event)

    def keyReleaseEvent(self, event):
        self.sendKeyEvent(event)
    
    def wheelEvent(self, event):
        x = event.x()
        y = event.y()
        flag = event.type()
        units = event.angleDelta()
        self.scrollevent['x'] = x
        self.scrollevent['y'] = y
        self.scrollevent['event'] = flag
        self.scrollevent['units'] = list(map(int, str(units).lstrip('PyQt5.QtCore.QPoint(').rstrip(')').split(',')))[1]
        self.mainObject.executeCommands(command.SCROLL, self.scrollevent)        

    def sendKeyEvent(self, event):
        key  = event.key()
        flag = event.type() 
        self.keyboardevent['key'] = key
        self.keyboardevent['flag'] = flag
        self.mainObject.executeCommands(command.KEY_EVENT, self.keyboardevent)
    
    def sendMouseEvent(self, event):
        time.sleep(0.04)
        x, y   = (event.pos().x(), event.pos().y()) 
        button = event.button()
        flag   = event.type()
        self.someevent['x'] = x
        self.someevent['y'] = y
        self.someevent['button'] = button
        self.someevent['flag'] = flag
        self.mainObject.executeCommands(command.POINTER_EVENT, self.someevent)
    
class remoteDisplayWindow(QMainWindow):
    def __init__(self, mainObject):
        super().__init__()
        self.mainObject = mainObject
        self.raise_()
        self.activateWindow()
    
    def closeEvent(self, event):
        self.mainObject.remoteWindowclosed = True
        self.mainObject.packet = b''
        self.mainObject.executeCommands(command.GENERAL_UPDATE, None)