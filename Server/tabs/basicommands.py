from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from commands import command


class BasicCommands(QWidget):
    def __init__(self, Window):
        super().__init__()
        self.obj = Window
        self.vbox = QVBoxLayout()
        self.addContents()
        self.setLayout(self.vbox)

    def addContents(self):
        
        # Basic Commands 
        
        rightpanesplitter = QSplitter(Qt.Vertical)
        commandWidget = QWidget()
        commandButtons = QGridLayout()
        commandWidget.setLayout(commandButtons)

        ## All Command buttons
        Screenshotbtn = QPushButton("Screenshot", self.obj)
        Screenshotbtn.setIcon(QtGui.QIcon("img/screenshot.png"))
        Screenshotbtn.setMaximumWidth(180)
        Screenshotbtn.setIconSize(QtCore.QSize(50,50))
        Screenshotbtn.clicked.connect(lambda: self.obj.executeCommands(command.SCREENSHOT, None))

        Clipboardbtn = QPushButton("Clipboard", self.obj)
        Clipboardbtn.setIcon(QtGui.QIcon("img/clipboard.png"))
        Clipboardbtn.setMaximumWidth(180)
        Clipboardbtn.setIconSize(QtCore.QSize(50,50))
        Clipboardbtn.clicked.connect(lambda: self.obj.executeCommands(command.CLIPBOARD, None))

        Shutdownbtn = QPushButton("Shutdown", self.obj)
        Shutdownbtn.setIcon(QtGui.QIcon("img/shutdown.png"))
        Shutdownbtn.setMaximumWidth(180)
        Shutdownbtn.setIconSize(QtCore.QSize(50,50))
        Shutdownbtn.clicked.connect(lambda: self.obj.executeCommands(command.SHUTDOWN, None))

        Logoffbtn = QPushButton("Restart", self.obj)
        Logoffbtn.setIcon(QtGui.QIcon("img/restart.png"))
        Logoffbtn.setMaximumWidth(180)
        Logoffbtn.setIconSize(QtCore.QSize(50,50))
        Logoffbtn.clicked.connect(lambda: self.obj.executeCommands(command.RESTART, None))

        UnlockUSBbtn = QPushButton("Unlock USB", self.obj)
        UnlockUSBbtn.setIcon(QtGui.QIcon("img/usb-unlock.png"))
        UnlockUSBbtn.setMaximumWidth(180)
        UnlockUSBbtn.setIconSize(QtCore.QSize(50,50))

        remotedesktopBtn = QPushButton("Remote Desktop", self.obj)
        remotedesktopBtn.setIcon(QtGui.QIcon("img/remote.png"))
        remotedesktopBtn.setMaximumWidth(180)
        remotedesktopBtn.setIconSize(QtCore.QSize(50,50))
        remotedesktopBtn.clicked.connect(lambda: self.remoteWindow())

        commandButtons.addWidget(Clipboardbtn, 0, 0)
        commandButtons.addWidget(Shutdownbtn, 0, 1)
        commandButtons.addWidget(Logoffbtn, 0, 2)
        commandButtons.addWidget(Screenshotbtn, 1, 0)
        commandButtons.addWidget(remotedesktopBtn, 1, 1)
        commandButtons.addWidget(UnlockUSBbtn, 1, 2)

        ## Buttons end

        ## Console output start
        label = QLabel("Output")
        self.obj.consoleoutput = QTextEdit()

        consoleoutputwidget = QWidget()
        consoleoutputlayout = QVBoxLayout()
        consoleoutputlayout.addWidget(label)
        consoleoutputlayout.addWidget(self.obj.consoleoutput)
        consoleoutputwidget.setLayout(consoleoutputlayout)

        ## Console output end
        

        rightpanesplitter.addWidget(commandWidget)
        rightpanesplitter.addWidget(consoleoutputwidget)
        
        self.vbox.addWidget(rightpanesplitter)

        # Basic Commands end
    def remoteWindow(self):
        self.obj.remotedisplaywindow.show()
        self.obj.executeCommands(command.FRAME_UPDATE, None)
