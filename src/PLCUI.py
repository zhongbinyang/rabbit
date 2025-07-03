import os
import sys
import threading
import time

from PyQt5.QtWidgets import QWidget
from Ui_PLC import *
from SwitchGroup import *
from Global import *



class PLCUI(QWidget):
    refreshSensor = pyqtSignal()
    style = '''
        QLabel#stateOn{
            color:rgb(255, 255, 255);
            background-color: rgb(0, 255, 0);
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
        }
        QLabel#stateOff{
            color:rgb(0, 0, 0);
            background-color: rgb(255, 0, 0);
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
        }
        
        QLabel#stateDefault{
            color:rgb(0, 0, 0);
            background-color: transparent;
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
        }
        QTextEdit#stateOn{
            color:rgb(255, 255, 255);
            background-color: rgb(0, 255, 0);
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
        }
        QTextEdit#stateOff{
            color:rgb(0, 0, 0);
            background-color: rgb(255, 0, 0);
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
        }
        
        QTextEdit#stateDefault{
            color:rgb(0, 0, 0);
            background-color: transparent;
            border-radius: 10px;
            border-style:solid;
            border-width:0px;
            border-color:rgb(117, 117, 117);
        }
        '''
    def __init__(self,parent=None):
        super(PLCUI, self).__init__(parent)
        self.ui = Ui_PLC()
        self.ui.setupUi(self)
        # self.ui.enableBox.hide()
        self.setStyleSheet(self.style)
        self.connectPLCSwitch = SwitchControl(self.ui.connectPLC)
        self.connectPLCSwitch.textNoChecked = "Connect"
        self.connectPLCSwitch.textChecked = "Disconnect"

        self.jackingSwitch = SwitchControl(self.ui.widgetJacking)
        self.jackingSwitch.textNoChecked = "CRADLE EXTRACT"
        self.jackingSwitch.textChecked = "CRADLE INSERT"

        # self.clamp1Switch = SwitchControl(self.ui.widgetClamp1)
        # self.clamp1Switch.textNoChecked = "Clamp X Out "
        # self.clamp1Switch.textChecked = "Clamp X In"
        #
        # self.clamp2Switch = SwitchControl(self.ui.widgetClamp2)
        # self.clamp2Switch.textNoChecked = "Clamp Y Out "
        # self.clamp2Switch.textChecked = "Clamp Y In"
        #
        # self.sideInsertion1Switch = SwitchControl(self.ui.widgetSideInsertion1)
        # self.sideInsertion1Switch.textNoChecked = "Power Out"
        # self.sideInsertion1Switch.textChecked = "Power In"
        #
        # self.sideInsertion2Switch = SwitchControl(self.ui.widgetSideInsertion2)
        # self.sideInsertion2Switch.textNoChecked = "Comm Out"
        # self.sideInsertion2Switch.textChecked = "Comm In"

        self.key1Switch = SwitchControl(self.ui.widgetClamp1)
        self.key1Switch.textNoChecked = "Reset Out"
        self.key1Switch.textChecked = "Reset In"

        self.key2Switch = SwitchControl(self.ui.widgetClamp2)
        self.key2Switch.textNoChecked = "LANE_SELECT Out"
        self.key2Switch.textChecked = "LANE_SELECT In"

        # self.startStopSwitch = SwitchControl(self.ui.widgetStartStop)
        # self.startStopSwitch.textNoChecked = "Stop"
        # self.startStopSwitch.textChecked = "Start"

        self.connectSignalSlot()
        self.sensorList = []
        self.sensorMap = {}
        self.xPosition = -999
        self.yPosition = -999
        self.zPosition = -999
        self.loadSensorIO()
        self.isRefresh = False
        self.isRUnThread = False
        self.thread = None
        if "PLCIP" in Global.Config:
            self.ui.ip.setText(Global.Config["PLCIP"])
        if "PLCPort" in Global.Config:
            self.ui.port.setValue(Global.Config["PLCPort"])
        self.refreshSensor.connect(self.refreshSensored)
        uithread = threading.Thread(target=self.autoStart)
        uithread.start()

    def initConnect(self):
        self.connectPLC(True, "")
        if PLC.modbus.is_open == False:
            self.connectPLC(False, "")
            self.connectPLC(True, "")
        if PLC.modbus.is_open == False:
            self.connectPLCSwitch.setToggled(False)
        else:
            self.connectPLCSwitch.setToggled(True)

    def loadSensorIO(self):
        self.sensorList = [
        "EMERGENCY STOP",
        "Lifter Down",
        "Lifter UP",
        "Clamp X Out",
        "Clamp X In",
        "Clamp Y Out",
        "Clamp Y In",
        "Power Out",
        "Power In",
        "Comm Out",
        "Comm In",
        "Tray In1",
        "Tray In2",
        "docking lever1 out",
        "docking lever1 in",
        "docking lever2 out",
        "docking lever2 in",
        "docking lever3 in",
        "docking lever3 out",
        "docking lever4 in",
        "docking lever4 out",
        ]
        self.sensorListEn = [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
        ]

        for i in range(0, 9):
            self.sensorList.append("")
            self.sensorListEn.append("")

        self.sensorList.append("Destaco Insert/Extract")
        self.sensorListEn.append("-")

        for i in range(0, 19):
            self.sensorList.append("")
            self.sensorListEn.append("")

        self.sensorList.append("Product Ready")
        self.sensorListEn.append("-")

        sensorLayout = QGridLayout(self.ui.sensor)
        sensorLayout.setSpacing(1)
        sensorLayout.setContentsMargins(0,0,0,0)
        self.ui.sensor.setLayout(sensorLayout)
        i = 0
        for d in range(len(self.sensorList)):
            name = self.sensorList[d]
            if name == "" or name == "备用":
                continue
            lab = QLabel(self.ui.sensor)
            lab.setText(self.sensorList[d] + "(" + self.sensorListEn[d]+")")
            lab.setAlignment(Qt.AlignLeft)
            lab.setAlignment(Qt.AlignVCenter)
            lab2 = QLabel(self.ui.sensor)
            lab2.setText("")
            lab2.setAlignment(Qt.AlignCenter)
            lab2.setMaximumSize(QSize(20, 20))
            lab2.setMinimumSize(QSize(20, 20))
            row = sensorLayout.rowCount()
            if i==2:
                row = row - 1
            sensor = {"label":lab2,"value":-1}
            self.sensorMap[name] = sensor
            sensorLayout.addWidget(lab2,row,0+i)
            sensorLayout.addWidget(lab,row,1+i)
            if i == 0:
                i = 2
            else:
                i = 0

    def autoStart(self):
        while True:
            try:
                if self.isRefresh:
                    time.sleep(0.2)
                    continue
                if len(self.sensorList):
                    ret = PLC.modbus.readMultipleCoil(10020,len(self.sensorList))
                    if ret[0]!= True:
                        continue
                    l = ret[1]
                    for i in range(len(self.sensorList)):
                        if i < len(l):
                            if self.sensorList[i] in self.sensorMap.keys():
                                self.sensorMap[self.sensorList[i]]["value"] = l[i]
                        else:
                            break
                self.refreshSensor.emit()
                time.sleep(0.3)
            except Exception as e:
                except_type, except_value, except_traceback = sys.exc_info()
                except_file = \
                    os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
                exc_dict = {
                    "Error Type": except_type,
                    "Error Info": str(except_value),
                    "Error File": except_file,
                    "Error Row": except_traceback.tb_lineno,
                }
                addLog(2,str(exc_dict))
                time.sleep(0.3)

    def refreshSensored(self):
        try:
            self.isRefresh = True
            for name in self.sensorList:
                if name == "" or name == "备用":
                    continue
                if self.sensorMap[name]["value"] == 1:
                    self.sensorMap[name]["label"].setObjectName("stateOn")
                    self.sensorMap[name]["label"].setStyleSheet("background-color: rgb(0, 255, 0);")
                elif self.sensorMap[name]["value"] == 0:
                    self.sensorMap[name]["label"].setObjectName("stateOff")
                    self.sensorMap[name]["label"].setStyleSheet("background-color: rgb(255, 0, 0);")
                else:
                    self.sensorMap[name]["label"].setObjectName("stateDefault")
                    self.sensorMap[name]["label"].setStyleSheet("background-color: transparent;")
            self.isRefresh = False
        except Exception as e:
            self.isRefresh = False
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": except_type,
                "Error Info": str(except_value),
                "Error File": except_file,
                "Error Row": except_traceback.tb_lineno,
            }
            addLog(2, str(exc_dict))


    def connectSignalSlot(self):
        self.connectPLCSwitch.toggled.connect(self.connectPLC)
        self.jackingSwitch.toggled.connect(self.startStopAction)
        # self.clamp1Switch.toggled.connect(self.clampX_action)
        # self.clamp2Switch.toggled.connect(self.clampY_action)
        # self.sideInsertion1Switch.toggled.connect(self.powerAction)
        # self.sideInsertion2Switch.toggled.connect(self.commAction)
        self.key1Switch.toggled.connect(self.resetAction)
        self.key2Switch.toggled.connect(self.lanAction)
        # self.startStopSwitch.toggled.connect(self.startStopAction)

    def connectPLC(self,value,text):
        ret = None
        if value == True:
            ip = self.ui.ip.text()
            port = self.ui.port.value()
            ret = PLC.connectPLC(ip,port)
        else:
            ret = PLC.disconnectPLC()
        if ret[0] == True:
            addLog(0,ret)
        else:
            addLog(2,ret)

    def lifterAction(self, value, text):
        ret = None
        if value == True:
            ret = PLC.lifterUp()
        else:
            ret = PLC.lifterDown()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def clampX_action(self, value, text):
        ret = None
        if value == False:
            ret = PLC.clampX_out()
        else:
            ret = PLC.clampX_in()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def clampY_action(self, value, text):
        ret = None
        if value == False:
            ret = PLC.clampY_out()
        else:
            ret = PLC.clampY_in()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def powerAction(self, value, text):
        ret = None
        if value == False:
            ret = PLC.powerOut()
        else:
            ret = PLC.powerIn()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def commAction(self, value, text):
        ret = None
        if value == False:
            ret = PLC.commOut()
        else:
            ret = PLC.commIn()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def resetAction(self, value, text):
        ret = None
        if value == False:
            ret = PLC.reset_off()
        else:
            ret = PLC.reset_on()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def lanAction(self, value, text):
        ret = None
        if value == False:
            ret = PLC.lane_select_off()
        else:
            ret = PLC.lane_select_on()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)

    def startStopAction(self, value, text):
        ret = None
        if value == False:
            ret = PLC.cradle_extracted()
        else:
            ret = PLC.cradle_inserted()
        if ret[0] == True:
            addLog(0, ret)
        else:
            addLog(2, ret)
