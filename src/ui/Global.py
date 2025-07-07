from PyQt5.QtCore import pyqtSignal, QObject

class Global(QObject):
    logSignal = pyqtSignal(int, str)
    calSignal = pyqtSignal()
    accImageSignal = pyqtSignal(str)
    angImageSignal = pyqtSignal(str)
    Config = {"PLCIP":"192.168.1.11","PLCPort":502}
    def __init__(self):
        super(Global, self).__init__()

    def setLogFunction(self,func):
        self.logSignal.connect(func)

    def setCalFunction(self,func):
        self.calSignal.connect(func)

    def setAccImageFunction(self,func):
        self.accImageSignal.connect(func)

    def setAngImageFunction(self, func):
        self.angImageSignal.connect(func)

Global = Global()
def addLog(type,log):
    Global.logSignal.emit(type,str(log))

def calButton():
    Global.calSignal.emit()

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def setAccImage(path):
    Global.accImageSignal.emit(path)

def setAngImage(path):
    Global.angImageSignal.emit(path)