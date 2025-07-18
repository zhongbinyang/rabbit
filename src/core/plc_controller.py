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
import json
from config.settings import IO_SETTING_FILE_PATH, ACTION_SETTING_FILE_PATH, IO_TYPE_FILE_PATH

class PLCController:
    """PLC控制器，提供高级控制功能"""
    
    def __init__(self):
        """初始化PLC控制器"""
        self.modbus = ModbusClient()
        self.is_connected = False
        self.host = PLC_CONFIG["host"]
        self.port = PLC_CONFIG["port"]
        self.lock = threading.RLock()  # 添加线程锁以保护Modbus通信
        self.delay_time = 1.0  # 操作之间的延迟时间，与PLCAPI一致
        self.io_setting = None
        
    

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
            self.is_connected = True
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
            if command_addr[0] == "M":
                return int(command_addr[1:])
            elif command_addr[0] == "H" and command_addr[1] == "D":
                return int(command_addr[2:])+41088
            elif command_addr[0] == "D":
                return int(command_addr[1:])
            else:
                return -1
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
        logger.info("Reading action configuration file in __init__...")
        try:
            with open(ACTION_SETTING_FILE_PATH, 'r') as f:
                self.action_config = json.load(f)
                logger.info("Action configuration file read successfully in __init__")
        except Exception as e:
            logger.error(f"Failed to read action configuration file in __init__: {e}")
            self.action_config = None

        # 读取动作配置（已移至__init__）
        if self.action_config is None:
            logger.error("Action configuration not loaded.")
            return False, "Action configuration not loaded."
        
        # 根据动作名称查找配置
        logger.info(f"Looking for configuration of action '{action}'...")
        action_config = next((item for item in self.action_config if item['action'] == action), None)
        if not action_config:
            logger.error(f"Configuration for action '{action}' not found")
            return False, f"Action '{action}' not found in action_config"
        else:
            logger.info(f"Configuration for action '{action}' found successfully")
            logger.info(f"Action '{action}' configuration details: {action_config}")

        # 获取动作配置中的readonly参数
        # 如果readonly为True，则不等待
        readonly = action_config.get('readonly', False)
        
        
        #
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
            logger.info(f"Address parsed: {command_addr} -> {addr}")
                    
            # 执行命令前记录
            logger.info(f"Starting command execution: {type} to address {addr}")

            is_check_value = False
            if type == 'write_multiple_coil':
                with self.lock:
                    ret = self.modbus.write_multiple_coil(addr, expected_value)
                    logger.info(f"write_multiple_coil result: {ret}")
            elif type == 'write_single_coil':
                with self.lock:
                    ret = self.modbus.write_single_coil(addr, expected_value)
                    logger.info(f"write_single_coil result: {ret}")
            elif type == 'read_multiple_coil':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_multiple_coil(addr, 2)
                    logger.info(f"read_multiple_coil result: {ret}")
            elif type == 'read_single_coil':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_single_coil(addr)
                    logger.info(f"read_single_coil result: {ret}")

            elif type == 'read_holding_registers':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_holding_registers(addr, 1)
                    logger.info(f"read_holding_registers result: {ret}")
        
            else:
                logger.error(f"Unknown command type: {type}")
                results.append((False, f"Unknown command type: {type}"))
                continue
            
            if not ret[0]:
                error_msg = f"{action} command failed: {ret[1]}"
                logger.error(error_msg)
                results.append((False, error_msg))
                break
            
            if expected_value is None or expected_value == -1 or expected_value == [-1]:
                is_check_value = False
                
            # is_check_value 为真时，循环读直到一致或超时
            if is_check_value:
                # 新增：对于读操作且checkvalue为真且值不一致时，循环读直到一致或超时
                if list(ret[1]) != list(expected_value):

                    isPass = False
                    if not readonly:
                        start_time = time.time()
                        while True:
                            time.sleep(0.2)
                            # 超时，退出循环
                            if time.time() - start_time >= delayseconds:
                                break
                            # 读取值
                            with self.lock:
                                if type == "read_multiple_coil":
                                    ret = self.modbus.read_multiple_coil(addr, 2)
                                elif type == "read_single_coil":
                                    ret = self.modbus.read_single_coil(addr)
                                elif type == "read_holding_registers":
                                    ret = self.modbus.read_holding_registers(addr, 1)
                                logger.info(f"Re-read {type} result: {ret}")
                                if not ret[0]:
                                    logger.error(f"Command {command_addr} executed failed during re-read: {ret[1]}")
                                    break
                                if list(ret[1]) == list(expected_value):
                                    logger.info(f"{type} value matches expected value after re-read.")
                                    isPass = True
                                    break
                                else:
                                    continue
                        if not isPass:
                            error_msg = f"Command {command_addr} executed failed: Actual value {ret[1]} does not match expected value {expected_value}"
                            logger.error(error_msg)
                            results.append((False, error_msg))
                            break
                           
                    else:
                        error_msg = f"Command {command_addr} executed failed: Actual value {ret[1]} does not match expected value {expected_value}"
                        logger.error(error_msg)
                        results.append((False, error_msg))
                        break
                else:
                    # 读取值与期望值一致，不等待
                    logger.info(f"Command {command_addr} executed successfully: Actual value {ret[1]} match expected value {expected_value}")
            # 非读操作，等待delayseconds秒
            else:
                time.sleep(delayseconds)

                
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
    def _execute_plc_command_set_control(self, action: str) -> Tuple[bool, str]:
        """
        执行PLC只写命令
        
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
        logger.info("Reading action configuration file in __init__...")
        try:
            with open(ACTION_SETTING_FILE_PATH, 'r') as f:
                self.action_config = json.load(f)
                logger.info("Action configuration file read successfully in __init__")
        except Exception as e:
            logger.error(f"Failed to read action configuration file in __init__: {e}")
            self.action_config = None

        # 读取动作配置（已移至__init__）
        if self.action_config is None:
            logger.error("Action configuration not loaded.")
            return False, "Action configuration not loaded."
        
        # 根据动作名称查找配置
        logger.info(f"Looking for configuration of action '{action}'...")
        action_config = next((item for item in self.action_config if item['action'] == action), None)
        if not action_config:
            logger.error(f"Configuration for action '{action}' not found")
            return False, f"Action '{action}' not found in action_config"
        else:
            logger.info(f"Configuration for action '{action}' found successfully")
            logger.info(f"Action '{action}' configuration details: {action_config}")

        # 存储每个命令的执行结果
        results = []
        total_commands = len(action_config['commands'])
        logger.info(f"Starting to execute {total_commands} PLC commands...")

        # 根据配置中的命令地址和值对执行操作
        for index, command in enumerate(action_config['commands'], 1):
            command_addr = command['command']
            expected_value = command['expected_value']
            timeout = command.get('delayseconds', 0)
            type = command['type']
            
            logger.info(f"[{index}/{total_commands}] Executing command: {type} - Address: {command_addr}, Expected value: {expected_value}")
        
            addr = self.get_plc_address_from_name(command_addr)
            logger.info(f"Address parsed: {command_addr} -> {addr}")
                    
            # 执行命令前记录
            logger.info(f"Starting command execution: {type} to address {addr}")

            is_check_value = False
            if type == 'write_multiple_coil':
                with self.lock:
                    ret = self.modbus.write_multiple_coil(addr, expected_value)
                    logger.info(f"write_multiple_coil result: {ret}")
            elif type == 'write_single_coil':
                with self.lock:
                    ret = self.modbus.write_single_coil(addr, expected_value)
                    logger.info(f"write_single_coil result: {ret}")
            elif type == 'read_holding_registers':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_holding_registers(addr, 1)
                    logger.info(f"read_holding_registers result: {ret}")
            
            elif type == 'read_multiple_coil':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_multiple_coil(addr, 2)
                    logger.info(f"read_multiple_coil result: {ret}")
            elif type == 'read_single_coil':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_single_coil(addr)
                    logger.info(f"read_single_coil result: {ret}")
        
            else:
                logger.error(f"Unknown command type: {type}")
                results.append((False, f"Unknown command type: {type}"))
                break
            
            if not ret[0]:
                error_msg = f"{action} command failed: {ret[1]}"
                logger.error(error_msg)
                results.append((False, error_msg))
                break

            if expected_value is None or expected_value == -1 or expected_value == [-1]:
                is_check_value = False

            # is_check_value 为真时，循环读直到一致或超时
            if is_check_value:
                # 新增：对于读操作且checkvalue为真且值不一致时，循环读直到一致或超时
                if list(ret[1]) != list(expected_value):
                    isPass = False
                    if timeout:
                        start_time = time.time()
                        while True:
                            time.sleep(0.2)
                            # 超时，退出循环
                            if time.time() - start_time >= timeout:
                                break
                            # 读取值
                            with self.lock:
                                if type == "read_multiple_coil":
                                    ret = self.modbus.read_multiple_coil(addr, 2)
                                elif type == "read_single_coil":
                                    ret = self.modbus.read_single_coil(addr)
                                elif type == "read_holding_registers":
                                    ret = self.modbus.read_holding_registers(addr, 1)
                                logger.info(f"Re-read {type} result: {ret}")
                                if not ret[0]:
                                    logger.error(f"Command {command_addr} executed failed during re-read: {ret[1]}")
                                    break
                                if list(ret[1]) == list(expected_value):
                                    logger.info(f"{type} value matches expected value after re-read.")
                                    isPass = True
                                    break
                                else:
                                    continue
                        if not isPass:
                            error_msg = f"Command {command_addr} executed failed: Actual value {ret[1]} does not match expected value {expected_value}"
                            logger.error(error_msg)
                            results.append((False, error_msg))
                            break
                    else:
                        error_msg = f"Command {command_addr} executed failed: Actual value {ret[1]} does not match expected value {expected_value}"
                        logger.error(error_msg)
                        results.append((False, error_msg))
                        break
                
            else:
                time.sleep(timeout)
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
    def _execute_plc_command_get_control(self, action: str) -> Tuple[bool, str, str]:
        """
        执行PLC只读命令
        
        Args:
            action: 动作名称
            
        Returns:
            操作结果(True/False, 消息)
        """
        logger.info(f"========== START EXECUTING PLC COMMAND: {action} ==========")
        
        if not self.is_connected:
            logger.error("Not connected to PLC, cannot execute command")
            return False, "Not connected to PLC", ""
        
        # 读取动作配置
        logger.info("Reading action configuration file in __init__...")
        try:
            with open(ACTION_SETTING_FILE_PATH, 'r') as f:
                self.action_config = json.load(f)
                logger.info("Action configuration file read successfully in __init__")
        except Exception as e:
            logger.error(f"Failed to read action configuration file in __init__: {e}")
            self.action_config = None

        # 读取动作配置（已移至__init__）
        if self.action_config is None:
            logger.error("Action configuration not loaded.")
            return False, "Action configuration not loaded.", ""
        
        # 根据动作名称查找配置
        logger.info(f"Looking for configuration of action '{action}'...")
        action_config = next((item for item in self.action_config if item['action'] == action), None)
        if not action_config:
            logger.error(f"Configuration for action '{action}' not found")
            return False, f"Action '{action}' not found in action_config", ""
        else:
            logger.info(f"Configuration for action '{action}' found successfully")
            logger.info(f"Action '{action}' configuration details: {action_config}")

        description = action_config['description']
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
            logger.info(f"Address parsed: {command_addr} -> {addr}")
                    
            # 执行命令前记录
            logger.info(f"Starting command execution: {type} to address {addr}")

            if type == 'read_holding_registers':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_holding_registers(addr, 1)
                    logger.info(f"read_holding_registers result: {ret}")
            
            elif type == 'read_multiple_coil':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_multiple_coil(addr, 2)
                    logger.info(f"read_multiple_coil result: {ret}")
            elif type == 'read_single_coil':
                is_check_value = True
                with self.lock:
                    ret = self.modbus.read_single_coil(addr)
                    logger.info(f"read_single_coil result: {ret}")

        
            else:
                is_check_value = False
                logger.error(f"Unknown command type: {type}")
                results.append((False, f"Unknown command type: {type}"))
                break
            
            if not ret[0]:
                error_msg = f"{action} command failed: {ret[1]}"
                logger.error(error_msg)
                results.append((False, error_msg))
                break
            
            if expected_value is None or expected_value == -1 or expected_value == [-1]:
                is_check_value = False
                
            # is_check_value 为真时，循环读直到一致或超时
            if is_check_value:
                # 新增：对于读操作且checkvalue为真且值不一致时，循环读直到一致或超时
                if list(ret[1]) != list(expected_value):
                    error_msg = f"Command {command_addr} executed failed: Actual value {ret[1]} does not match expected value {expected_value}"
                    logger.error(error_msg)
                    results.append((False, error_msg))
                    break
                

                
            success_msg = f"Command {command_addr} executed successfully"    
            logger.info(success_msg)
            results.append((True, success_msg))
        
        # 如果有任何命令失败，整个操作视为失败
        success_count = sum(1 for success, _ in results if success)
        logger.info(f"Command execution completed. Total: {len(results)}, Success: {success_count}, Failed: {len(results) - success_count}")
        
        first_part = ""
        second_part = ""
        if '_' in description:
            idx = description.rfind('_')
            first_part = description[:idx]
            second_part = description[idx+1:]

        if any(not success for success, _ in results):
            # 找出第一个失败的命令信息
            for success, msg in results:
                if not success:
                    logger.error(f"Operation failed: {msg}")
                    logger.info(f"========== PLC COMMAND EXECUTION ENDED: {action} [FAILED] ==========")
                    return False, msg, second_part, second_part
        
        # 全部命令成功执行
        success_msg = f"{action} command executed successfully"
        logger.info(success_msg)
        logger.info(f"========== PLC COMMAND EXECUTION ENDED: {action} [SUCCESS] ==========")
        return True, success_msg, first_part
    
    @handle_exception
    def _set_control(self, control_name: str, control_state: str) -> Tuple[bool, str]:
        """
        执行PLC通用命令
        
        Args:
            action: 动作名称
            
        Returns:
            操作结果(True/False, 消息)
        """
        control_name = control_name + "_" + control_state
        return self._execute_plc_command_set_control(control_name)
    
    @handle_exception
    def _get_control(self, control_name: str) -> Tuple[bool, str, str]:
        """
        执行PLC通用命令
        
        Args:
            action: 动作名称
            
        Returns:
            操作结果(True/False, 消息)
        """
        control_name = control_name + "_" + "state"
        return self._execute_plc_command_get_control(control_name)

# 单例模式
plc_controller = PLCController() 