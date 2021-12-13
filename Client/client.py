from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget
from twisted.internet import protocol, endpoints, defer
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint
from twisted.internet.protocol import Factory, Protocol, ServerFactory
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from core import *
from commands import command
import input_event as _input
import subprocess
import pyautogui
import qt5reactor
import time
import sys


app = QApplication(sys.argv)

qt5reactor.install()

class Window(Protocol, QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self._buffer = ''
        self.packet = b''
        self.expected_len = 0
        self._array     = QByteArray( )
        self._buffer    = QBuffer(self._array)
        self._buffer.open(QIODevice.WriteOnly)
        self.basic()
        self.InitWindow()
        self.keyboard   = _input.Keyboard( )
        self.mouse      = _input.Mouse( )

    # overridden from protocol
    def connectionMade(self):
        self.transport.writeSequence((pack(command.USERNAME, "Shobhit"), b'\r\n'))
        # self.sendGeneralInfo()

    # overridden from protocol
    def connectionLost(self, reason):
        print('Connection Lost')

    # overridden from protocol
    def dataReceived(self, data):
            strbuf = data.decode("utf-8")
            strbuf = strbuf.rstrip('\r\n')
            buf = strbuf.split('\r\n')
            for i in buf:
                try:
                    cmd = eval(i)
                except:
                    print(i)
                for key in cmd.keys(): 
                    args = cmd[key]
                self.handler(key, args)
                self.packet = b''
    
    def sendGeneralInfo(self, flag):
        info = {}
        if flag == None:
            info['machinename'] = getMachineName()
            info['os'] = getOperatingSystemVersion()
            info['username'] = getCurrentUsername()
            info['localip'] = getLocalIP()
        info['uptime'] = getUptime()
        info['cpu'] = getCPUUsage()
        info['memory'] = getMemoryUsage()
        info['localip'] = getLocalIP()
        info['currentapp'] = getCurrentWindowTitle()
        pixmap = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId())
        pixmap = pixmap.scaled(300, 210, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        pixmap.save(self._buffer, 'jpeg')
        pixdata = self._buffer.data()
        info['pixdata'] = bytes(pixdata)
        if flag == 1:
            self.sendData(command.GENERAL_UPDATE, info)
        else:
            self.sendData(command.GENERAL, info)
        self._array.clear()
        self._buffer.close()

    def shellCommand(self, args):
        print(args)

    # handle received request
    def handler(self, key, args):
        if key == command.FRAME_UPDATE:
            self.sharescreen(args)
        if key == command.POINTER_EVENT:
            self.pointerEvent(args)
        if key == command.KEY_EVENT:
            self.keyevent(args)
        if key == command.SCROLL:
            self.scrollevent(args)
        if key == command.GENERAL:
            self.sendGeneralInfo(None)
        if key == command.GENERAL_UPDATE:
            self.sendGeneralInfo(1)
    
    def scrollevent(self, args):
        self.mouse.move(args['x'], args['y'])
        pyautogui.scroll(args['units'])
    
    def keyevent(self, args):
        key = args['key']
        flag = args['flag']
        if flag == 6:
            self.keyboard.press(key)
        elif flag == 7:
            self.keyboard.release(key)
        else:
            self.keyboard.press(key)
            self.keyboard.release(key)
        
    def pointerEvent(self, args):
        x, y = args['x'], args['y']
        flag = args['flag']
        button = args['button']
        if flag == 5:
            self.mouse.move(x, y)
        elif flag == 2:
            self.mouse.press(x, y, button)
        elif flag == 3:
            self.mouse.release(x, y, button)
        elif flag == 4:
            self.mouse.press(x, y, button)
            self.mouse.release(x, y, button)
        

    def sharescreen(self, args):
        pixmap = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId())
        # if args != None:
        #     width, height = args['width'], args['height']
        #     if self.screen_height > height or self.screen_width > width:
        #         self.scale = True
        #         self.screen_width, self.screen_height = width, height
        # if self.scale:
        #     pixmap.scaled(self.screen_width, self.screen_height, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        pixmap.save(self._buffer, 'jpeg')
        pixdata = self._buffer.data()
        self.sendData(command.FRAME_UPDATE, pixdata)
        self._array.clear()
        self._buffer.close()

    def sendData(self, flag, args):
        if flag == command.FRAME_UPDATE:
            self.transport.writeSequence((pack(command.FRAME_UPDATE, args), b'\r\n'))
        elif flag == command.GENERAL:
            self.transport.writeSequence((pack(command.GENERAL, args), b'\r\n'))
        elif flag == command.GENERAL_UPDATE:
            self.transport.writeSequence((pack(command.GENERAL_UPDATE, args), b'\r\n'))



    # packs data in format "lengthof data to be sent@{command : command related data}"

    def basic(self):
        self.title = "LiveTrack"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 300
        self.scale = False
        screen_resolution = app.desktop().screenGeometry()
        self.screen_width = screen_resolution.width()
        self.screen_height = screen_resolution.height()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("spy.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        displayWidget = QWidget( )
        vbox   = QVBoxLayout(displayWidget)
        self.setCentralWidget(displayWidget)

if __name__ == '__main__':
    from twisted.internet import reactor
    window = Window()
    point = TCP4ClientEndpoint(reactor, "127.0.0.1", 8000)
    d = connectProtocol(point, Window())
    
    reactor.run()