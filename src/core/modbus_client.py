import sys

from modbus_tk import modbus_tcp, modbus_rtu
import modbus_tk.defines as cst

import serial
import serial.tools.list_ports
import struct
import threading
from utils.exceptions import PLCConnectionError, PLCTimeoutError, handle_exception
from config.settings import PLC_CONFIG
from typing import Tuple, Any, List
from utils.logger import logger



class ModbusClient:
    """Modbus通信客户端，支持RTU和TCP协议"""
    
    def __init__(self):
        """初始化Modbus客户端"""
        self.mod = None
        self.ser = None
        self.is_open = False
        self.lock = threading.RLock()

    @handle_exception
    def open_modbus_rtu(self, port: str, baudrate: int = 115200, 
                     data_bits: int = 8, stop_bit: int = 1,
                     parity: str = 'N') -> Tuple[bool, str]:
        """
        打开Modbus RTU连接
        
        Args:
            port: 串口端口
            baudrate: 波特率，默认115200
            data_bits: 数据位，默认8
            stop_bit: 停止位，默认1
            parity: 校验位，默认'N'
            
        Returns:
            成功返回(True, "Connected")，失败返回(False, 错误信息)
        """
        try:
            if self.is_open:
                return True, "已连接"
                
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=data_bits,
                stopbits=stop_bit,
                parity=parity
            )
            self.mod = modbus_rtu.RtuMaster(self.ser)
            self.mod.set_timeout(PLC_CONFIG["timeout"])
            self.is_open = True
            logger.info(f"Modbus RTU Connected Successfully: {port}")
            return True, "Connected"
        except Exception as e:
            self.is_open = False
            logger.error(f"Modbus RTU Connection Failed: {str(e)}")
            raise PLCConnectionError(f"Modbus RTU Connection Failed: {str(e)}")

    @handle_exception
    def open_modbus_tcp(self, host: str, port: int = 502) -> Tuple[bool, str]:
        """
        打开Modbus TCP连接
        
        Args:
            host: 主机地址
            port: 端口号，默认502
            
        Returns:
            成功返回(True, "Connected")，失败返回(False, 错误信息)
        """
        try:
            if self.is_open:
                return True, "Connected"
                
            self.mod = modbus_tcp.TcpMaster(host=host, port=port)
            self.mod.set_timeout(PLC_CONFIG["timeout"])
            self.mod.open()
            self.is_open = True
            logger.info(f"Modbus TCP Connected Successfully: {host}:{port}")
            return True, "Connected"
        except Exception as e:
            self.is_open = False
            logger.error(f"Modbus TCP Connection Failed: {str(e)}")
            raise PLCConnectionError(f"Modbus TCP Connection Failed: {str(e)}")

    @handle_exception
    def close(self) -> Tuple[bool, str]:
        """
        关闭Modbus连接
        
        Returns:
            成功返回(True, "关闭成功")，失败返回(False, 错误信息)
        """
        try:
            if self.ser is not None:
                self.ser.close()
            if self.mod is not None:
                self.mod.close()
            self.is_open = False
            logger.info("Modbus Connection Closed Successfully")
            return True, "Closed Successfully"
        except Exception as e:
            self.is_open = False
            logger.error(f"Modbus Connection Closed Failed: {str(e)}")
            return False, f"Closed Failed: {str(e)}"

    @handle_exception
    def read_single_coil(self, address: int) -> Tuple[bool, Any]:
        """
        读取单个线圈
        
        Args:
            address: 寄存器地址
            
        Returns:
            成功返回(True, 值)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.READ_COILS, address, 1)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Read Coil Failed - Address {address}: {str(e)}")
            return False, str(e)

    @handle_exception
    def read_multiple_coil(self, address: int, count: int) -> Tuple[bool, Any]:
        """
        读取多个线圈
        
        Args:
            address: 起始寄存器地址
            count: 读取的线圈数量
            
        Returns:
            成功返回(True, 值元组)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.READ_COILS, address, count)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Read Multiple Coils Failed - Address {address}, Count {count}: {str(e)}")
            return False, str(e)

    @handle_exception
    def write_single_coil(self, address: int, value: int) -> Tuple[bool, Any]:
        """
        写入单个线圈
        
        Args:
            address: 寄存器地址
            value: 写入的值（0或1）
            
        Returns:
            成功返回(True, 值)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_SINGLE_COIL, address, output_value=value)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Write Coil Failed - Address {address}, Value {value}: {str(e)}")
            return False, str(e)

    @handle_exception
    def write_multiple_coil(self, address: int, values: List[int]) -> Tuple[bool, Any]:
        """
        写入多个线圈
        
        Args:
            address: 起始寄存器地址
            values: 写入的值列表
            
        Returns:
            成功返回(True, 值)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_MULTIPLE_COILS, address, output_value=values)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Write Multiple Coils Failed - Address {address}: {str(e)}")
            return False, str(e)

    @handle_exception
    def read_holding_registers(self, address: int, count: int) -> Tuple[bool, Any]:
        """
        读取保持寄存器
        
        Args:
            address: 起始寄存器地址
            count: 读取的寄存器数量
            
        Returns:
            成功返回(True, 值元组)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.READ_HOLDING_REGISTERS, address, count)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Read Holding Registers Failed - Address {address}, Count {count}: {str(e)}")
            return False, str(e)

    @handle_exception
    def write_single_register(self, address: int, value: int) -> Tuple[bool, Any]:
        """
        写入单个寄存器
        
        Args:
            address: 寄存器地址
            value: 写入的值
            
        Returns:
            成功返回(True, 值)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_SINGLE_REGISTER, address, output_value=value)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Write Single Register Failed - Address {address}, Value {value}: {str(e)}")
            return False, str(e)

    @handle_exception
    def write_multiple_registers(self, address: int, values: List[int]) -> Tuple[bool, Any]:
        """
        写入多个寄存器
        
        Args:
            address: 起始寄存器地址
            values: 写入的值列表
            
        Returns:
            成功返回(True, 值)，失败返回(False, 错误信息)
        """
        try:
            self.lock.acquire()
            ret = self.mod.execute(1, cst.WRITE_MULTIPLE_REGISTERS, address, output_value=values)
            self.lock.release()
            return True, ret
        except Exception as e:
            self.lock.release()
            logger.error(f"Write Multiple Registers Failed - Address {address}: {str(e)}")
            return False, str(e)

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
            if ret1[0] == False:
                return ret1
            ret2 = self.handleAddress(start_addr)
            if ret2[0] == False:
                return ret2
            ret3 = self.writeMultipleRegister(ret2[1], ret1[1])
            return ret3
        except Exception as ex:
            return False, str(ex)

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
            if ret2[0] == False:
                return ret2
            ret = self.readHoldingRegisters(ret2[1], 4)
            if ret[0] != True:
                return ret
            ret = self.DCBAToDouble(ret[1])
            return ret
        except Exception as ex:
            return False, str(ex)

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
            return True, valueByte[0]
        except Exception as ex:
            return False, str(ex)

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
            return True, tuple(reversed(valueByte))
        except Exception as ex:
            return False, str(ex)

    def binaryToFloat(self, binary_str):
        try:
            binary_data = bytes(
                [int(binary_str[i:i + 8], 2) for i in
                 range(0, len(binary_str), 8)])
            decimal_num = struct.unpack('!f', binary_data)[0]
            return True, decimal_num
        except Exception as ex:
            return False, str(ex)

    def floatToBinary(self, num):
        try:
            binary_data = struct.pack('!f', num)
            binary_str = ''.join(format(byte, '08b') for byte in binary_data)
            return True, binary_str
        except Exception as ex:
            return False, str(ex)

    def binaryToDouble(self, binary_str):
        try:
            binary_data = bytes(
                [int(binary_str[i:i + 8], 2) for i in
                 range(0, len(binary_str), 8)])
            decimal_num = struct.unpack('!d', binary_data)[0]
            return True, decimal_num
        except Exception as ex:
            return False, str(ex)

    def doubleToBinary(self, num):
        try:
            binary_data = struct.pack('!d', num)
            binary_str = ''.join(format(byte, '08b') for byte in binary_data)
            return True, binary_str
        except Exception as ex:
            return False, str(ex)

    def getModbusValue(self, binary_str):
        try:
            value = []
            if len(binary_str) < 64:
                return False, "binary_str is short then 64" + str(
                    len(binary_str))
            for i in range(4):
                strValue = binary_str[-16:]
                value.append(int(int(strValue, 2)))
                binary_str = binary_str[:-16]
            return True, value
        except Exception as ex:
            return False, str(ex)

    def handleFloatData(self, floatData):
        try:
            binary_str = self.floatToBinary(floatData)
            value = self.getModbusValue(binary_str)
            return True, value
        except Exception as ex:
            return False, str(ex)

    def handleDoubleData(self, doubleData):
        try:
            binary_str = self.doubleToBinary(doubleData)
            if binary_str[0] == False:
                return binary_str
            value = self.getModbusValue(binary_str[1])
            return True, value
        except Exception as ex:
            return False, str(ex)

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
            return True, addr
        except Exception as ex:
            return False, str(ex)