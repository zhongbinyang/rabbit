import json
import os
import signal
import datetime

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont

from Ui_MainFrom import *
from PyQt5.QtWidgets import QMainWindow

from PLCUI import *
from Global import *

import platform

class MainFrom(QMainWindow):
    style = '''
    QWidget{background-color: rgb(245, 245, 245);}
QPushButton{background-color: rgb(210, 210, 210);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(117, 117, 117);
            font-weight:bold;}
QSpinBox{background-color: rgb(210, 210, 210);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(117, 117, 117);
            font-weight:bold;}
QDoubleSpinBox{background-color: rgb(210, 210, 210);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(117, 117, 117);
            font-weight:bold;}
QScrollArea{background-color: rgb(210, 210, 210);
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
            }
QPushButton:hover{ background-color: rgb(0, 255, 255);}
QPushButton:pressed{ background-color: rgb(0, 205, 205);}
QGroupBox{background-color: rgb(245, 245, 245);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(117, 117, 117);
            }
QTextEdit{background-color: rgb(235, 235, 235);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(117, 117, 117);
            }
QComboBox{background-color: transparent;
            border-radius: 10px;
            border-style:solid;
            border-width:2px;
            border-color:rgb(176, 176, 176);
            }
QComboBox::drop-down{background-color: rgb(176, 176, 176);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(176, 176, 176);
            }
QLabel{ 
            font-weight:bold;
            background-color: rgb(245, 245, 245);}
QLineEdit{  background-color: rgb(225, 225, 225);
            border-radius: 10px;
            border-style:solid;
            border-width:1px;
            border-color:rgb(117, 117, 117);
            font-weight:bold;
            background-color: rgb(245, 245, 245);}
    '''
    def __init__(self,parent=None):
        super(MainFrom, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowTitle("FT_V1.0.0.8")
        self.ui.labInformation.setText("Bojay PLC UI (Gorilla FT) (Moose FT)")
        if os.path.exists(os.getcwd() + "/Config.json"):
            file = open(os.getcwd() + "/Config.json", "r+")
            Global.Config = json.load(file)
            file.close()
        self.plcUI = PLCUI()
        self.ui.tabWidget.addTab(self.plcUI,"PLC")
        Global.setLogFunction(self.addLog)
        import platform
        if platform.system() == "Darwin":
            font = QFont("PingFang SC", 9)
        elif platform.system() == "Windows":
            font = QFont("Microsoft YaHei", 9)
        else:
            font = QFont("Arial", 9)
        self.setFont(font)
        self.setStyleSheet(self.style)
        # self.showMaximized()
        self.timerConnect = QTimer()
        self.timerConnect.timeout.connect(self.initConnect)
        self.timerConnect.start(100)


    def closeEvent(self, QCloseEvent ):
        Global.Config["PLCIP"] = self.plcUI.ui.ip.text()
        Global.Config["PLCPort"] = self.plcUI.ui.port.value()
        path = os.getcwd() + "/Config.json"
        file = open(path, "w+")
        json.dump(Global.Config, file)
        file.close()
        PLC.disconnectPLC()
        os.kill(os.getpid(), signal.SIGTERM)
    def initConnect(self):
        self.timerConnect.stop()
        self.plcUI.initConnect()

    def addLog(self,type,log):
        path = os.getcwd() + "/Log/"
        if not os.path.exists(path):
            os.mkdir(path)
        filenames = [f for f in os.listdir(path) if
                     os.path.isfile(os.path.join(path, f))]
        filenames = [file for file in filenames if file.endswith('.log')]
        filenames.sort()
        if len(filenames) > 10:
            for i in range(len(filenames)-10):
                os.remove(path+filenames[i])
        path = path + datetime.datetime.now().strftime(
            '/%Y-%m-%d-%H.log')
        path.replace("\\", "/")
        writeStr = ""
        if type == 0:
            writeStr = "Info  " + datetime.datetime.now().strftime("%H:%M:%S-%f ") + log
            self.ui.textEdit.setTextColor(QColor(0,0,0))
            self.ui.textEdit.append(writeStr)
        elif type == 1:
            writeStr = "Warning  " + datetime.datetime.now().strftime(
                "%H:%M:%S-%f ") + log
            self.ui.textEdit.setTextColor(QColor(255, 255, 0))
            self.ui.textEdit.append(writeStr)
        elif type == 2:
            writeStr = "Error  " + datetime.datetime.now().strftime(
                "%H:%M:%S-%f ") + log
            self.ui.textEdit.setTextColor(QColor(255, 0, 0))
            self.ui.textEdit.append(writeStr)
        self.ui.textEdit.moveCursor(QTextCursor.End)
        file = open(path, "a+")
        file.write(writeStr+"\n")
        file.close()
