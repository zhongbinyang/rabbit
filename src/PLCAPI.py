import json
import sys

from modbus_tk import modbus_tcp, modbus_rtu
import modbus_tk.defines as cst

import datetime
import serial
import serial.tools.list_ports
import binascii
import struct
import time
import os
import threading


class BojayModbus:
    mod = None
    ser = None
    BOJAYOK = True
    BOJAYNG = False

    def __init__(self):
        self.is_open = False
        self.lock = threading.RLock()

    def openModbusRTU(self, Port, Baudrate=115200, DataBits=8, StopBit=1,
                      Parity='N'):
        '''
                Index     : 1
                Function  : open ModbusRTU
                Param     : Port, Baudrate=115200, DataBits=8, StopBit=1, Parity='N'
                Return    : "PASS","Connected"
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            if self.is_open:
                return self.BOJAYOK, "Connected"
            self.ser = serial.Serial(port=Port,
                                     baudrate=Baudrate,
                                     bytesize=DataBits,
                                     stopbits=StopBit,
                                     parity=Parity)
            self.mod = modbus_rtu.RtuMaster(self.ser)
            self.mod.set_timeout(3.0)
            self.is_open = True
            return self.BOJAYOK, "Connected"
        except Exception as ex:
            self.is_open = False
            except_type, except_value, except_traceback = sys.exc_info()
            return self.BOJAYNG, str(except_value)

    def openModbusTCP(self, host, port=502):
        '''
                Index     : 2
                Function  : open ModbusTCP
                Param     : host, port=502
                Return    : "PASS", "Connected"
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            if self.is_open:
                return self.BOJAYOK, "Connected"
            self.mod = modbus_tcp.TcpMaster(host=host, port=port)
            self.mod.set_timeout(3.0)
            self.mod.open()
            self.is_open = True
            return self.BOJAYOK, "Connected"
        except Exception as ex:
            self.is_open = False
            except_type, except_value, except_traceback = sys.exc_info()
            return self.BOJAYNG, str(except_value)

    def close(self):
        '''
                Index     : 3
                Function  : close serial port
                Param     : no use
                Return    : "PASS", ret
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            if self.ser != None:
                ret = self.ser.close()
            if self.mod != None:
                ret = self.mod.close()
            self.is_open = False
            ret = "Close Successful"
            return self.BOJAYOK, ret
        except Exception as ex:
            self.is_open = False
            return self.BOJAYNG, str(ex)

    def readSingleCoil(self, start_addr):
        '''
                Index     : 4
                Function  : read Single Coil
                Param     : start_addr
                Return    : "PASS", ret = 0 or 1
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.READ_COILS, start_addr, 1)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def readMultipleCoil(self, start_addr, value):
        '''
                Index     : 5
                Function  : read Multiple Coil
                Param     : start_addr,value
                Return    : "PASS", ret=(0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1)
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.READ_COILS, start_addr, value)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def writeSingleCoil(self, start_addr, value):
        '''
                Index     : 6
                Function  : write Single Coil
                Param     : start_addr, value
                Return    : "PASS", ret=0 or 1
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_SINGLE_COIL, start_addr,
                                   output_value=value)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def writeMultipleCoil(self, start_addr, value):
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_MULTIPLE_COILS, start_addr,
                                   output_value=value)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def readHoldingRegisters(self, start_addr, length):
        '''
                Index     : 7
                Function  : read Holding Registers
                Param     : start_addr, length
                Return    : "PASS", ret=(0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1)
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.READ_HOLDING_REGISTERS, start_addr,
                                   length)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def writeSingleRegister(self, start_addr, value):
        '''
                Index     : 8
                Function  : write Single Register
                Param     : start_addr, value
                Return    : "PASS", ret=0 or 1
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_SINGLE_REGISTER, start_addr,
                                   output_value=value)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def writeMultipleRegister(self, start_addr, value):
        '''
                Index     : 9
                Function  : write Multiple Register
                Param     : start_addr, value
                Return    : "PASS", ret=(0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1,0 or 1)
                            False,str(e): str(e) is expect fail message
        '''
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_MULTIPLE_REGISTERS, start_addr,
                                   output_value=value)
            self.lock.release()
            return self.BOJAYOK, ret
        except Exception as ex:
            self.lock.release()
            return self.BOJAYNG, str(ex)

    def writeDoubleValue(self, start_addr, value):
        '''
                Index     : 10
                Function  : write Double Value
                Param     : start_addr, value
                Return    : "PASS", ret=0 or 1
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            ret1 = self.doubleToDCBA(value)
            if ret1[0] == self.BOJAYNG:
                return ret1
            ret2 = self.handleAddress(start_addr)
            if ret2[0] == self.BOJAYNG:
                return ret2
            ret3 = self.writeMultipleRegister(ret2[1], ret1[1])
            return ret3
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def readDoubleValue(self, start_addr):
        '''
                Index     : 11
                Function  : read Double Value
                Param     : start_addr
                Return    : "PASS", ret = (0~65535,0~65535,0~65535,0~65535)
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            ret2 = self.handleAddress(start_addr)
            if ret2[0] == self.BOJAYNG:
                return ret2
            ret = self.readHoldingRegisters(ret2[1], 4)
            if ret[0] != self.BOJAYOK:
                return ret
            ret = self.DCBAToDouble(ret[1])
            return ret
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def DCBAToDouble(self, value):
        '''
                Index     : 12
                Function  : DCBA To Double
                Param     : value
                Return    : "PASS", com_list: Returns all serial port numbers in the form of a list
                            False, "No serial port found": No serial port found
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            valueByte = struct.unpack('!d',
                                      struct.pack('!HHHH', value[3], value[2],
                                                  value[1], value[0]))
            return self.BOJAYOK, valueByte[0]
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def doubleToDCBA(self, value):
        '''
                Index     : 13
                Function  : refresh serial port
                Param     : no use
                Return    : "PASS", com_list: Returns all serial port numbers in the form of a list
                            False, "No serial port found": No serial port found
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            valueByte = struct.unpack('!HHHH', struct.pack('!d', value))
            return self.BOJAYOK, tuple(reversed(valueByte))
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def binaryToFloat(self, binary_str):
        try:
            binary_data = bytes(
                [int(binary_str[i:i + 8], 2) for i in
                 range(0, len(binary_str), 8)])
            decimal_num = struct.unpack('!f', binary_data)[0]
            return self.BOJAYOK, decimal_num
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def floatToBinary(self, num):
        try:
            binary_data = struct.pack('!f', num)
            binary_str = ''.join(format(byte, '08b') for byte in binary_data)
            return self.BOJAYOK, binary_str
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def binaryToDouble(self, binary_str):
        try:
            binary_data = bytes(
                [int(binary_str[i:i + 8], 2) for i in
                 range(0, len(binary_str), 8)])
            decimal_num = struct.unpack('!d', binary_data)[0]
            return self.BOJAYOK, decimal_num
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def doubleToBinary(self, num):
        try:
            binary_data = struct.pack('!d', num)
            binary_str = ''.join(format(byte, '08b') for byte in binary_data)
            return self.BOJAYOK, binary_str
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def getModbusValue(self, binary_str):
        try:
            value = []
            if len(binary_str) < 64:
                return self.BOJAYNG, "binary_str is short then 64" + str(
                    len(binary_str))
            for i in range(4):
                strValue = binary_str[-16:]
                value.append(int(int(strValue, 2)))
                binary_str = binary_str[:-16]
            return self.BOJAYOK, value
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def handleFloatData(self, floatData):
        try:
            binary_str = self.floatToBinary(floatData)
            value = self.getModbusValue(binary_str)
            return self.BOJAYOK, value
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def handleDoubleData(self, doubleData):
        try:
            binary_str = self.doubleToBinary(doubleData)
            if binary_str[0] == self.BOJAYNG:
                return binary_str
            value = self.getModbusValue(binary_str[1])
            return self.BOJAYOK, value
        except Exception as ex:
            return self.BOJAYNG, str(ex)

    def handleAddress(self, start_addr):
        '''
                Index     : 14
                Function  : refresh serial port
                Param     : no use
                Return    : "PASS", com_list: Returns all serial port numbers in the form of a list
                            False, "No serial port found": No serial port found
                            False,str(e): str(e) is open port expect fail message
        '''
        try:
            addr = start_addr
            # addr = start_addr + 0
            return self.BOJAYOK, addr
        except Exception as ex:
            return self.BOJAYNG, str(ex)


class AddressMap:
    def __init__(self):
        self.plcAddress = {}
        self.plcAddress["LifterUP"] = "M10000"
        self.plcAddress["LifterDown"] = "M10001"
        self.plcAddress["ClampX_In"] = "M10002"
        self.plcAddress["ClampX_Out"] = "M10003"
        self.plcAddress["ClampY_In"] = "M10004"
        self.plcAddress["ClampY_Out"] = "M10005"
        self.plcAddress["PowerIn"] = "M10006"
        self.plcAddress["PowerOut"] = "M10007"
        self.plcAddress["CommIn"] = "M10008"
        self.plcAddress["CommOut"] = "M10009"
        self.plcAddress["reset"] = "M10010"
        self.plcAddress["lane_select"] = "M10011"
        self.plcAddress["cradle"] = "M10060"

        self.plcAddress["cradle_inserted_state"] = "M10070"
        self.plcAddress["docking_lever1_out_sensor"] = "M10033"
        self.plcAddress["ClampY_Out_Sensor"] = "M10025"
        self.plcAddress["ClampY_In_Sensor"] = "M10026"
        self.plcAddress["PowerOut_Sensor"] = "M10027"
        self.plcAddress["PowerIn_Sensor"] = "M10028"
        self.plcAddress["CommOut_Sensor"] = "M10029"
        self.plcAddress["CommIn_Sensor"] = "M10030"

    def getPLCAddress(self, name):
        if name in self.plcAddress:
            value = self.plcAddress[name]
            if len(value) > 2:
                if value[0] == "M":
                    address = int(value[1:])
                    return address
                elif value[0] == "H" and value[1] == "D":
                    address = int(value[2:])+41088
                    return address
                elif value[0] == "D":
                    address = int(value[1:])
                    return address
        return -1

class PLC:
    modbus = BojayModbus()
    def __init__(self):
        self.delay_time = 1
        try:
            self.addressMap = AddressMap()
            self.axisList = ["X","Y","Z"]
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
            os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False,json.dumps(exc_dict)

    def waitActionComplete(self, addressName, result, actionName, timeout):
        address = self.addressMap.getPLCAddress(addressName)
        startTime = time.time()
        while True:
            ret = self.modbus.readMultipleCoil(address, 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False, f"Read Coil Error_address:{address} error:{str(ret[1])}"
            elif ret[1] == result:
                return True, f"Set {actionName} Successful_address"
            elif time.time() - startTime > timeout:
                return False, f"The {actionName} failed. Please check the equipment. => address:{address} state:{str(ret[1])} result:{result}"

    def connectPLC(self,host = "192.168.6.6",port=502):
        try:
            ret = self.modbus.openModbusTCP(host, port)
            if ret[0] == self.modbus.BOJAYOK:
                return ret[0],"Connect PLC Successful "+host+":"+str(port)
            else:
                return ret[0],"Connect PLC Fail,Error:"+str(ret[1])
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def disconnectPLC(self):
        try:
            ret = self.modbus.close()
            return ret
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def lifterUp(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "LifterUP"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(1,0))
            if ret[0] != self.modbus.BOJAYOK:
                return False," Set Lifter Up Error:" + str(ret[1])
            time.sleep(self.delay_time)
            address = self.addressMap.getPLCAddress("LifterDown_Sensor")
            ret = self.modbus.readMultipleCoil(address, 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False," Lifter Up Read Coil Error:" + str(ret[1])
            if ret[1] != (0,1):
                return False, " Lifter Up Read Coil Fail:" + str(ret[1])
            return True, "Set Lifter Up Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def lifterDown(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "LifterUP"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(0,1))
            if ret[0] != self.modbus.BOJAYOK:
                return False," Set Lifter Down Down Error:" + str(ret[1])
            time.sleep(self.delay_time)
            address = self.addressMap.getPLCAddress("LifterDown_Sensor")
            ret = self.modbus.readMultipleCoil(address, 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Lifter Down Read Coil Error:" + str(ret[1])
            if ret[1] != (1,0):
                return False, "Lifter Down Read Coil Fail:" + str(ret[1])
            return True, "Set Lifter Down Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def clampX_in(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "ClampX_In"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(1,0))
            if ret[0] != self.modbus.BOJAYOK:
                return False," Set Clamp X In Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("ClampX_Out_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Clamp X In Read Coil Error:" + str(ret[1])
            if ret[1] != (0,1):
                return False, "Clamp X In Read Coil Fail:" + str(ret[1])
            return True, "Set Clamp X In Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def clampX_out(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "ClampX_In"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(0,1))
            if ret[0] != self.modbus.BOJAYOK:
                return False," Set Clamp X Out Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("ClampX_Out_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Clamp X Out Read Coil Error:" + str(ret[1])
            if ret[1] != (1,0):
                return False, "Clamp X Out Read Coil Fail:" + str(ret[1])
            return True, "Set Clamp X Out Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def clampY_in(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "ClampY_In"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(1,0))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Clamp Y In Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("ClampY_Out_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Clamp Y In Read Coil Error:" + str(ret[1])
            if ret[1] != (0,1):
                return False, "Clamp Y In Read Coil Fail:" + str(ret[1])
            return True, "Set Clamp Y In Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def clampY_out(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "ClampY_In"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(0,1))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Clamp Y Out Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("ClampY_Out_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Clamp Y Out Read Coil Error:" + str(ret[1])
            if ret[1] != (1,0):
                return False, "Clamp Y Out Read Coil Fail:" + str(ret[1])
            return True, "Set Clamp Y Out Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def powerIn(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "PowerIn"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(1,0))
            if ret[0] != self.modbus.BOJAYOK:
                return False," Set Power In Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("PowerOut_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Power In Read Coil Error:" + str(ret[1])
            if ret[1] != (0,1):
                return False, "Power In Read Coil Fail:" + str(ret[1])
            return True, "Set Power In Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def powerOut(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "PowerIn"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(0,1))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Power Out Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("PowerOut_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False, "Power Out Read Coil Error:" + str(ret[1])
            if ret[1] != (1, 0):
                return False, "Power Out Read Coil Fail:" + str(ret[1])
            return True, "Set Power Out Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def commIn(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "CommIn"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(1,0))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Comm In Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("CommOut_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Comm In Read Coil Error:" + str(ret[1])
            if ret[1] != (0,1):
                return False, "Comm In Read Coil Fail:" + str(ret[1])
            return True, "Set Comm In Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def commOut(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "CommIn"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(0,1))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Comm Out Error:" + str(ret[1])
            time.sleep(self.delay_time)
            ret = self.modbus.readMultipleCoil(self.addressMap.getPLCAddress("CommOut_Sensor"), 2)
            if ret[0] != self.modbus.BOJAYOK:
                return False, "Comm Out Read Coil Error:" + str(ret[1])
            if ret[1] != (1, 0):
                return False, "Comm Out Read Coil Fail:" + str(ret[1])
            return True, "Set Comm Out Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def reset_on(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "reset"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeSingleCoil(address,1)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Reset In Error:" + str(ret[1])
            time.sleep(self.delay_time)
            return True, "Set Reset In Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def reset_off(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "reset"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeSingleCoil(address,0)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Reset Out Error:" + str(ret[1])
            time.sleep(self.delay_time)
            return True, "Set Reset Out Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def lane_select_on(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "lane_select"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeSingleCoil(address,1)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Lan In Error:" + str(ret[1])
            time.sleep(self.delay_time)
            return True, "Set Lan In Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def lane_select_off(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "lane_select"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeSingleCoil(address,0)
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set Lan Out Error:" + str(ret[1])
            time.sleep(self.delay_time)
            return True, "Set Lan Out Successful"
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def cradle_inserted(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "cradle"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(1,0))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set CRADLE INSERT Error:" + str(ret[1])
            time.sleep(1)

            return self.waitActionComplete("cradle_inserted_state", (1,0), "cradle_inserted", 15)

        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def cradle_extracted(self):
        try:
            if self.modbus.is_open == False:
                return False,"PLC is not connect"
            command = "cradle"
            address = self.addressMap.getPLCAddress(command)
            ret = self.modbus.writeMultipleCoil(address,(0,1))
            if ret[0] != self.modbus.BOJAYOK:
                return False,"Set CRADLE EXTRACT Error:" + str(ret[1])
            time.sleep(1)

            return self.waitActionComplete("cradle_inserted_state", (0,1), "cradle_inserted", 15)
        except Exception as e:
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = \
                os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "Error Type": str(except_type),
                "Error Info": str(except_value),
                "Error File": str(except_file),
                "Error Row": str(except_traceback.tb_lineno)
            }
            return False, json.dumps(exc_dict)

    def get_cradle_state(self):
        if self.modbus.is_open == False:
            return "inserted", 1, "PLC is not connect"

        address = self.addressMap.getPLCAddress("cradle_inserted_state")
        ret = self.modbus.readMultipleCoil(address, 2)
        if ret[0] != self.modbus.BOJAYOK:
            return "inserted", 1, "get_cradle_state Read Coil Error:" + str(ret[1])
        if ret[1] == (1, 0):
            return "inserted", 0, ""
        if ret[1] == (0, 1):
            return "extracted", 0, ""
        return "inserted", 1, f"The status is incorrect. Please check the equipment. => address:{address} state:{str(ret[1])}"

    def get_destaco_state(self):
        if self.modbus.is_open == False:
            return "inserted", 1, "PLC is not connect"

        address = self.addressMap.getPLCAddress("docking_lever1_out_sensor")
        ret = self.modbus.readMultipleCoil(address, 8)
        if ret[0] != self.modbus.BOJAYOK:
            return "inserted", 1, "get_destaco_state Read Coil Error:" + str(ret[1])
        if ret[1] == (0,1, 0,1, 1,0, 1,0):
            return "inserted", 0, ""
        if ret[1] == (1,0, 1,0, 0,1, 0,1):
            return "extracted", 0, ""
        return "inserted", 1, f"The status is incorrect. Please check the equipment. => address:{address} state:{ret[1]}"

    def get_reset_state(self):
        if self.modbus.is_open == False:
            return "on", 1, "PLC is not connect"

        ret = self.modbus.readSingleCoil(self.addressMap.getPLCAddress("reset"))
        if ret[0] != self.modbus.BOJAYOK:
            return "on", 1, "get_reset_state Read Coil Error:" + str(ret[1])
        if ret[1] == (1,):
            return "on", 0, ""
        else:
            return "off", 0, ""

    def get_lane_select_state(self):
        if self.modbus.is_open == False:
            return "on", 1, "PLC is not connect"

        ret = self.modbus.readSingleCoil(self.addressMap.getPLCAddress("lane_select"))
        if ret[0] != self.modbus.BOJAYOK:
            return "on", 1, "get_lane_select Read Coil Error:" + str(ret[1])
        if ret[1] == (1,):
            return "on", 0, ""
        else:
            return "off", 0, ""

    def get_plc_firmware(self):
        if self.modbus.is_open == False:
            return "0.0"

        ret = self.modbus.readHoldingRegisters(50, 1)
        if ret[0] != self.modbus.BOJAYOK:
            return "0.0"

        ver = format(ret[1][0] / 10, ".1f")
        return ver
