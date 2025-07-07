import json
import sys

from modbus_tk import modbus_tcp, modbus_rtu
import modbus_tk.defines as cst

import time
import os
from core.modbus_client import ModbusClient
from config.settings import PLC_CONFIG
from utils.logger import logger
from utils.exceptions import handle_exception
from typing import Tuple, Any, List, Dict, Optional, Union
import threading

class AddressMap:
    """PLC地址映射，将名称映射到地址"""

    def __init__(self):
        """初始化PLC地址映射"""
        self.address_map = {
            # 控制指令对 - 每个功能有相反的两个命令
            "lifter_up": 10000,     # 升降台上升/下降是一对命令 (M10000)
            "clampx_in": 10002,     # X轴夹钳收回/伸出是一对命令 (M10002)
            "clampy_in": 10004,     # Y轴夹钳收回/伸出是一对命令 (M10004)
            "power_in": 10006,      # 电源插入/拔出是一对命令 (M10006)
            "comm_in": 10008,       # 通信口插入/拔出是一对命令 (M10008)
            "reset": 10010,         # 重置按钮开/关是一对命令 (M10010)
            "lane_select": 10011,   # 通道选择开/关是一对命令 (M10011)
            "cradle": 10060,        # 托架插入/拔出是一对命令 (M10060)
            
            # 状态读取
            "lifter_state": 10020,  # 升降台状态对应传感器 
            "clampx_state": 10023,  # X轴夹钳状态对应传感器
            "clampy_state": 10025,  # Y轴夹钳状态对应传感器 (M10025)
            "power_state": 10027,   # 电源状态对应传感器 (M10027)
            "comm_state": 10029,    # 通信口状态对应传感器 (M10029)
            "reset_state": 10010,   # 重置按钮状态 (复用控制地址 M10010)
            "lane_select_state": 10011, # 通道选择状态 (复用控制地址 M10011)
            "cradle_state": 10070,  # 托架状态对应传感器 (M10070)
            
            # 固件版本
            "plc_firmware": 50,     # 固件版本寄存器地址
        }

    def get_plc_address(self, name: str) -> int:
        """
        获取PLC地址
        
        Args:
            name: 地址名称
            
        Returns:
            寄存器地址
            
        Raises:
            KeyError: 当地址名称不存在时
        """
        if name not in self.address_map:
            raise KeyError(f"Address name not found: {name}")
        return self.address_map[name]

class PLCController:
    """PLC控制器，提供高级控制功能"""
    
    def __init__(self):
        """初始化PLC控制器"""
        self.modbus = ModbusClient()
        self.address_map = AddressMap()
        self.is_connected = False
        self.host = PLC_CONFIG["host"]
        self.port = PLC_CONFIG["port"]
        self.lock = threading.RLock()  # 添加线程锁以保护Modbus通信
        self.delay_time = 1.0  # 操作之间的延迟时间，与PLCAPI一致
    

    def wait_action_complete(self, address_name: str, expected_value: tuple, 
                            action_name: str, timeout: int = 15) -> Tuple[bool, str]:
        """
        等待PLC动作完成
        
        Args:
            address_name: 地址名称
            expected_value: 期望的值元组 (如(0,1)或(1,0))
            action_name: 动作名称(用于日志)
            timeout: 超时时间(秒)
            
        Returns:
            操作结果(True/False, 消息)
            
        Raises:
            PLCTimeoutError: 操作超时
        """
        start_time = time.time()
        addr = self.address_map.get_plc_address(address_name)
        
        while True:
            if time.time() - start_time > timeout:
                error_msg = f"{action_name} Operation timeout"
                logger.error(error_msg)
                return False, error_msg
            
            with self.lock:
                ret = self.modbus.read_multiple_coil(addr, 2)  # 读取两个连续的线圈状态
            
            if not ret[0]:
                logger.warning(f"Read {action_name} status failed: {ret[1]}")
                time.sleep(0.1)
                continue
                
            if ret[1] == expected_value:
                logger.info(f"{action_name} Operation successful")
                return True, f"{action_name} Operation successful"
            
            time.sleep(0.1)

    @handle_exception
    def connect_plc(self, host: Optional[str] = None, port: Optional[int] = None) -> Tuple[bool, str]:
        """
        连接到PLC
        
        Args:
            host: PLC主机地址，默认使用配置值
            port: PLC端口，默认使用配置值
            
        Returns:
            连接结果(True/False, 消息)
        """
        if host is None:
            host = self.host
        if port is None:
            port = self.port
            
        if self.is_connected:
            return True, f"Connected to PLC {host}:{port}"
        
        ret = self.modbus.open_modbus_tcp(host, port)
        if ret[0]:
            self.is_connected = True
            self.host = host
            self.port = port
            logger.info(f"Connected to PLC {host}:{port}")
            return True, f"Connected to PLC {host}:{port}"
        else:
            self.is_connected = False
            logger.error(f"Connect to PLC failed: {ret[1]}")
            return False, f"Connect to PLC failed: {ret[1]}"
    
    @handle_exception
    def disconnect_plc(self) -> Tuple[bool, str]:
        """
        断开PLC连接
        
        Returns:
            断开结果(True/False, 消息)
        """
        ret = self.modbus.close()
        if ret[0]:
            self.is_connected = False
            logger.info("Disconnect PLC successfully")
            return True, "Disconnect PLC successfully"
        else:
            logger.error(f"Disconnect PLC failed: {ret[1]}")
            return False, f"Disconnect PLC failed: {ret[1]}"
    
    def get_plc_address_from_name(self, command_addr: str) -> int:
        # 如果是以字母开头，去掉字母前缀
        if command_addr[0].isalpha():
            return int(command_addr[1:])
        else:
            return int(command_addr)
        
    @handle_exception
    def _execute_plc_command(self, action: str) -> Tuple[bool, str]:
        """
        执行PLC通用命令
        
        Args:
            action: 动作名称
            
        Returns:
            操作结果(True/False, 消息)
        """
        logger.info(f"========== START EXECUTING PLC COMMAND: {action} ==========")
        
        if not self.is_connected:
            logger.error("Not connected to PLC, cannot execute command")
            return False, "Not connected to PLC"
        
        # 读取动作配置
        logger.info("Reading action configuration file...")
        try:
            with open(os.path.join(os.path.dirname(__file__), '..', 'api', 'static', 'PLC_IO_List_A01_grouped.json'), 'r') as f:
                action_config = json.load(f)
                logger.info("Action configuration file read successfully")
        except Exception as e:
            logger.error(f"Failed to read action configuration file: {e}")
            return False, f"Failed to read action config: {str(e)}"
            
        # 根据动作名称查找配置
        logger.info(f"Looking for configuration of action '{action}'...")
        action_config = next((item for item in action_config if item['action'] == action), None)
        if not action_config:
            logger.error(f"Configuration for action '{action}' not found")
            return False, f"Action '{action}' not found in action_config"
        else:
            logger.info(f"Configuration for action '{action}' found successfully")
            logger.debug(f"Action '{action}' configuration details: {action_config}")

        # 存储每个命令的执行结果
        results = []
        total_commands = len(action_config['commands'])
        logger.info(f"Starting to execute {total_commands} PLC commands...")

        # 根据配置中的命令地址和值对执行操作
        for index, command in enumerate(action_config['commands'], 1):
            command_addr = command['command']
            expected_value = command['expected_value']
            delayseconds = command.get('delayseconds', 0)
            type = command['type']
            
            logger.info(f"[{index}/{total_commands}] Executing command: {type} - Address: {command_addr}, Expected value: {expected_value}")
        
            addr = self.get_plc_address_from_name(command_addr)
            logger.debug(f"Address parsed: {command_addr} -> {addr}")
                    
            # 执行命令前记录
            logger.info(f"Starting command execution: {type} to address {addr}")

            if type == 'write_multiple_coil':
                with self.lock:
                    ret = self.modbus.write_multiple_coil(addr, expected_value)
                    logger.debug(f"write_multiple_coil result: {ret}")
            elif type == 'write_single_coil':
                with self.lock:
                    ret = self.modbus.write_single_coil(addr, expected_value)
                    logger.debug(f"write_single_coil result: {ret}")
            elif type == 'read_multiple_coil':
                with self.lock:
                    ret = self.modbus.read_multiple_coil(addr, 2)
                    logger.debug(f"read_multiple_coil result: {ret}")
            elif type == 'read_single_coil':
                with self.lock:
                    ret = self.modbus.read_single_coil(addr, 2)
                    logger.debug(f"read_single_coil result: {ret}")
            else:
                logger.error(f"Unknown command type: {type}")
                results.append((False, f"Unknown command type: {type}"))
                continue
            
            if not ret[0]:
                error_msg = f"{action} command failed: {ret[1]}"
                logger.error(error_msg)
                results.append((False, error_msg))
                continue
            
            # 等待操作完成
            if delayseconds > 0:
                    logger.info(f"Waiting for operation to complete, delay: {delayseconds} seconds")
            time.sleep(delayseconds)
            logger.info(f"Delay completed")
            
            if ret[1] != expected_value:
                    error_msg = f"{action} command failed: Actual value {ret[1]} does not match expected value {expected_value}"
                    logger.error(error_msg)
                    results.append((False, error_msg))
                    continue
                
            success_msg = f"Command {command_addr} executed successfully"    
            logger.info(success_msg)
            results.append((True, success_msg))
        
        # 如果有任何命令失败，整个操作视为失败
        success_count = sum(1 for success, _ in results if success)
        logger.info(f"Command execution completed. Total: {len(results)}, Success: {success_count}, Failed: {len(results) - success_count}")
        
        if any(not success for success, _ in results):
            # 找出第一个失败的命令信息
            for success, msg in results:
                if not success:
                    logger.error(f"Operation failed: {msg}")
                    logger.info(f"========== PLC COMMAND EXECUTION ENDED: {action} [FAILED] ==========")
                    return False, msg
        
        # 全部命令成功执行
        success_msg = f"{action} command executed successfully"
        logger.info(success_msg)
        logger.info(f"========== PLC COMMAND EXECUTION ENDED: {action} [SUCCESS] ==========")
        return True, success_msg
    
    @handle_exception
    def lifter_up(self) -> Tuple[bool, str]:
        """
        升降台上升命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "lifter_up"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (1, 0))  # 设置上升=1,下降=0
            
        if not ret[0]:
            logger.error(f"Lifter up command failed: {ret[1]}")
            return False, f"Lifter up command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("lifter_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read lifter state failed: {ret[1]}")
            return False, f"Read lifter state failed: {ret[1]}"
            
        if ret[1] != (1, 0):  # 期望状态:上升=1,下降=0
            logger.error(f"Lifter up operation failed, current state: {ret[1]}")
            return False, f"Lifter up operation failed, current state: {ret[1]}"
            
        return True, "Lifter up operation successful"

    @handle_exception
    def lifter_down(self) -> Tuple[bool, str]:
        """
        升降台下降命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "lifter_up"  # 使用基础地址
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (0, 1))  # 设置上升=0,下降=1
            
        if not ret[0]:
            logger.error(f"Lifter down command failed: {ret[1]}")
            return False, f"Lifter down command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("lifter_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read lifter state failed: {ret[1]}")
            return False, f"Read lifter state failed: {ret[1]}"
            
        if ret[1] != (0, 1):  # 期望状态:上升=0,下降=1
            logger.error(f"Lifter down operation failed, current state: {ret[1]}")
            return False, f"Lifter down operation failed, current state: {ret[1]}"
            
        return True, "Lifter down operation successful"
    

    @handle_exception
    def clamp_x_in(self) -> Tuple[bool, str]:
        """
        X轴夹钳收回命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "clampx_in"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (1, 0))  # 设置收回=1,伸出=0
            
        if not ret[0]:
            logger.error(f"Clamp x in command failed: {ret[1]}")
            return False, f"Clamp x in command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("clampx_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read clamp x state failed: {ret[1]}")
            return False, f"Read clamp x state failed: {ret[1]}"
            
        if ret[1] != (0, 1):  # 期望状态根据实际情况设置
            logger.error(f"Clamp x in operation failed, current state: {ret[1]}")
            return False, f"Clamp x in operation failed, current state: {ret[1]}"
            
        return True, "Clamp x in operation successful"

    @handle_exception
    def clamp_x_out(self) -> Tuple[bool, str]:
        """
        X轴夹钳伸出命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "clampx_in"  # 使用基础地址
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (0, 1))  # 设置收回=0,伸出=1
            
        if not ret[0]:
            logger.error(f"Clamp x out command failed: {ret[1]}")
            return False, f"Clamp x out command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("clampx_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read clamp x state failed: {ret[1]}")
            return False, f"Read clamp x state failed: {ret[1]}"
            
        if ret[1] != (1, 0):  # 期望状态根据实际情况设置
            logger.error(f"Clamp x out operation failed, current state: {ret[1]}")
            return False, f"Clamp x out operation failed, current state: {ret[1]}"
            
        return True, "Clamp x out operation successful"
    

    


    @handle_exception
    def clamp_y_in(self) -> Tuple[bool, str]:
        """
        Y轴夹钳收回命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "clampy_in"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (1, 0))  # 设置收回=1,伸出=0
            
        if not ret[0]:
            logger.error(f"Clamp y in command failed: {ret[1]}")
            return False, f"Clamp y in command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("clampy_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read clamp y state failed: {ret[1]}")
            return False, f"Read clamp y state failed: {ret[1]}"
            
        if ret[1] != (0, 1):  # 期望状态根据实际情况设置
            logger.error(f"Clamp y in operation failed, current state: {ret[1]}")
            return False, f"Clamp y in operation failed, current state: {ret[1]}"
            
        return True, "Clamp y in operation successful"
    
    @handle_exception
    def clamp_y_out(self) -> Tuple[bool, str]:
        """
        Y轴夹钳伸出命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "clampy_in"  # 使用基础地址
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (0, 1))  # 设置收回=0,伸出=1
            
        if not ret[0]:
            logger.error(f"Clamp y out command failed: {ret[1]}")
            return False, f"Clamp y out command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("clampy_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read clamp y state failed: {ret[1]}")
            return False, f"Read clamp y state failed: {ret[1]}"
            
        if ret[1] != (1, 0):  # 期望状态根据实际情况设置
            logger.error(f"Clamp y out operation failed, current state: {ret[1]}")
            return False, f"Clamp y out operation failed, current state: {ret[1]}"
            
        return True, "Clamp y out operation successful"
    
    @handle_exception
    def power_in(self) -> Tuple[bool, str]:
        """
        电源插入命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "power_in"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (1, 0))  # 设置插入=1,拔出=0
            
        if not ret[0]:
            logger.error(f"Power in command failed: {ret[1]}")
            return False, f"Power in command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("power_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read power state failed: {ret[1]}")
            return False, f"Read power state failed: {ret[1]}"
            
        if ret[1] != (0, 1):  # 期望状态根据实际情况设置
            logger.error(f"Power in operation failed, current state: {ret[1]}")
            return False, f"Power in operation failed, current state: {ret[1]}"
            
        return True, "Power in operation successful"
    
    @handle_exception
    def power_out(self) -> Tuple[bool, str]:
        """
        电源拔出命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "power_in"  # 使用基础地址
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (0, 1))  # 设置插入=0,拔出=1
            
        if not ret[0]:
            logger.error(f"Power out command failed: {ret[1]}")
            return False, f"Power out command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("power_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read power state failed: {ret[1]}")
            return False, f"Read power state failed: {ret[1]}"
            
        if ret[1] != (1, 0):  # 期望状态根据实际情况设置
            logger.error(f"Power out operation failed, current state: {ret[1]}")
            return False, f"Power out operation failed, current state: {ret[1]}"
            
        return True, "Power out operation successful"
    
    @handle_exception
    def comm_in(self) -> Tuple[bool, str]:
        """
        通信口插入命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "comm_in"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (1, 0))  # 设置插入=1,拔出=0
            
        if not ret[0]:
            logger.error(f"Comm in command failed: {ret[1]}")
            return False, f"Comm in command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("comm_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read comm state failed: {ret[1]}")
            return False, f"Read comm state failed: {ret[1]}"
            
        if ret[1] != (0, 1):  # 期望状态根据实际情况设置
            logger.error(f"Comm in operation failed, current state: {ret[1]}")
            return False, f"Comm in operation failed, current state: {ret[1]}"
            
        return True, "Comm in operation successful"
    
    @handle_exception
    def comm_out(self) -> Tuple[bool, str]:
        """
        通信口拔出命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "comm_in"  # 使用基础地址
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (0, 1))  # 设置插入=0,拔出=1
            
        if not ret[0]:
            logger.error(f"Comm out command failed: {ret[1]}")
            return False, f"Comm out command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        
        addr = self.address_map.get_plc_address("comm_state")
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read comm state failed: {ret[1]}")
            return False, f"Read comm state failed: {ret[1]}"
            
        if ret[1] != (1, 0):  # 期望状态根据实际情况设置
            logger.error(f"Comm out operation failed, current state: {ret[1]}")
            return False, f"Comm out operation failed, current state: {ret[1]}"
            
        return True, "Comm out operation successful"
    
    @handle_exception
    def reset_on(self) -> Tuple[bool, str]:
        """
        重置按钮按下命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "reset"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_single_coil(addr, 1)  # 按照PLCAPI.py的写法使用单线圈
            
        if not ret[0]:
            logger.error(f"Reset on command failed: {ret[1]}")
            return False, f"Reset on command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        return True, "Reset on operation successful"
    
    @handle_exception
    def reset_off(self) -> Tuple[bool, str]:
        """
        重置按钮释放命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "reset"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_single_coil(addr, 0)  # 按照PLCAPI.py的写法使用单线圈
            
        if not ret[0]:
            logger.error(f"Reset off command failed: {ret[1]}")
            return False, f"Reset off command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        return True, "Reset off operation successful"
    
    @handle_exception
    def lane_select_on(self) -> Tuple[bool, str]:
        """
        通道选择按下命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "lane_select"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_single_coil(addr, 1)  # 按照PLCAPI.py的写法使用单线圈
            
        if not ret[0]:
            logger.error(f"Lane select on command failed: {ret[1]}")
            return False, f"Lane select on command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        return True, "Lane select on operation successful"
    
    @handle_exception
    def lane_select_off(self) -> Tuple[bool, str]:
        """
        通道选择释放命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "lane_select"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_single_coil(addr, 0)  # 按照PLCAPI.py的写法使用单线圈
            
        if not ret[0]:
            logger.error(f"Lane select off command failed: {ret[1]}")
            return False, f"Lane select off command failed: {ret[1]}"
            
        time.sleep(self.delay_time)
        return True, "Lane select off operation successful"
    
    @handle_exception
    def cradle_inserted(self) -> Tuple[bool, str]:
        """
        托架插入命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "cradle"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (1, 0))  # 设置插入=1,拔出=0
            
        if not ret[0]:
            logger.error(f"Cradle inserted command failed: {ret[1]}")
            return False, f"Cradle inserted command failed: {ret[1]}"
            
        time.sleep(1)  # 特殊等待时间
        
        # 等待动作完成
        return self.wait_action_complete("cradle_state", (1, 0), "Cradle inserted", 15)
    
    @handle_exception
    def cradle_extracted(self) -> Tuple[bool, str]:
        """
        托架拔出命令
        
        Returns:
            操作结果(True/False, 消息)
        """
        if not self.is_connected:
            return False, "Not connected to PLC"
            
        command = "cradle"
        addr = self.address_map.get_plc_address(command)
        
        with self.lock:
            ret = self.modbus.write_multiple_coil(addr, (0, 1))  # 设置插入=0,拔出=1
            
        if not ret[0]:
            logger.error(f"Cradle extracted command failed: {ret[1]}")
            return False, f"Cradle extracted command failed: {ret[1]}"
            
        time.sleep(1)  # 特殊等待时间
        
        # 等待动作完成
        return self.wait_action_complete("cradle_state", (0, 1), "Cradle extracted", 15)
    
    @handle_exception
    def get_cradle_state(self) -> Tuple[str, int, str]:
        """
        获取托架状态
        
        Returns:
            状态名称, 错误码(0=正常), 错误消息
        """
        if not self.is_connected:
            return "inserted", 1, "Not connected to PLC"
            
        addr = self.address_map.get_plc_address("cradle_state")
        
        with self.lock:
            ret = self.modbus.read_multiple_coil(addr, 2)
            
        if not ret[0]:
            logger.error(f"Read cradle state failed: {ret[1]}")
            return "inserted", 1, f"Read cradle state failed: {ret[1]}"
            
        if ret[1] == (1, 0):
            return "inserted", 0, ""
        elif ret[1] == (0, 1):
            return "extracted", 0, ""
        else:
            error_msg = f"Cradle state abnormal: {ret[1]}"
            logger.error(error_msg)
            return "inserted", 1, error_msg
    
    @handle_exception
    def get_plc_firmware(self) -> str:
        """
        获取PLC固件版本
        
        Returns:
            版本字符串
        """
        if not self.is_connected:
            return "0.0"
            
        addr = self.address_map.get_plc_address("plc_firmware")
        
        with self.lock:
            ret = self.modbus.read_holding_registers(addr, 1)
            
        if not ret[0]:
            logger.error(f"Read firmware version failed: {ret[1]}")
            return "0.0"
            
        # 将寄存器值转换为版本字符串
        ver = format(ret[1][0] / 10, ".1f")
        return ver

    @handle_exception
    def get_reset_state(self) -> Tuple[str, int, str]:
        """
        获取重置按钮状态
        
        Returns:
            状态名称, 错误码(0=正常), 错误消息
        """
        if not self.is_connected:
            return "on", 1, "Not connected to PLC"

        addr = self.address_map.get_plc_address("reset_state")
        
        with self.lock:
            ret = self.modbus.read_single_coil(addr)
            
        if not ret[0]:
            logger.error(f"Read reset state failed: {ret[1]}")
            return "on", 1, f"Read reset state failed: {ret[1]}"
            
        if ret[1] == (1,):
            return "on", 0, ""
        else:
            return "off", 0, ""
    
    @handle_exception
    def get_lane_select_state(self) -> Tuple[str, int, str]:
        """
        获取通道选择状态
        
        Returns:
            状态名称, 错误码(0=正常), 错误消息
        """
        if not self.is_connected:
            return "on", 1, "Not connected to PLC"

        addr = self.address_map.get_plc_address("lane_select_state")
        
        with self.lock:
            ret = self.modbus.read_single_coil(addr)
            
        if not ret[0]:
            logger.error(f"Read lane select state failed: {ret[1]}")
            return "on", 1, f"Read lane select state failed: {ret[1]}"
            
        if ret[1] == (1,):
            return "on", 0, ""
        else:
            return "off", 0, ""

# 单例模式
plc_controller = PLCController() 