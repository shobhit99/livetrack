from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from commands import command

class Shell(QWidget):
    def __init__(self, Window):
        super().__init__()
        self.obj = Window
        self.vbox = QVBoxLayout()
        self.addContents()
        self.setLayout(self.vbox)

    def addContents(self):

        
        hbox = QHBoxLayout()
        commandinput = QLineEdit()
        commandinput.returnPressed.connect(lambda : self.obj.executeCommands('custom', commandinput.text()))

        execBtn = QPushButton("Execute")
        execBtn.setIcon(QtGui.QIcon("img/shell.png"))
        execBtn.clicked.connect(lambda : self.obj.executeCommands('custom', commandinput.text()))

        clearBtn = QPushButton("")
        clearBtn.setIcon(QtGui.QIcon("img/clear.png"))
        clearBtn.clicked.connect(lambda : self.obj.outputConsole.setText(""))

        hbox.addWidget(commandinput)
        hbox.addWidget(execBtn)
        hbox.addWidget(clearBtn)

        self.obj.outputConsole = QTextEdit()
        self.obj.outputConsole.setStyleSheet('background-color: #2C2C2C; color:#00FF00')

        
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.obj.outputConsole)