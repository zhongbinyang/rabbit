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
from config.settings import PLC_IO_LIST_A01_GROUPED_PATH

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
        logger.info("Reading action configuration file...")
        try:
            with open(PLC_IO_LIST_A01_GROUPED_PATH, 'r') as f:
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
            logger.info(f"Action '{action}' configuration details: {action_config}")

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

            checkvalue = False
            if type == 'write_multiple_coil':
                with self.lock:
                    ret = self.modbus.write_multiple_coil(addr, expected_value)
                    logger.info(f"write_multiple_coil result: {ret}")
            elif type == 'write_single_coil':
                with self.lock:
                    ret = self.modbus.write_single_coil(addr, expected_value)
                    logger.info(f"write_single_coil result: {ret}")
            elif type == 'read_multiple_coil':
                checkvalue = True
                with self.lock:
                    ret = self.modbus.read_multiple_coil(addr, 2)
                    logger.info(f"read_multiple_coil result: {ret}")
            elif type == 'read_single_coil':
                checkvalue = True
                with self.lock:
                    ret = self.modbus.read_single_coil(addr)
                    logger.info(f"read_single_coil result: {ret}")
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
            
            if checkvalue and list(ret[1]) != list(expected_value):
                    error_msg = f"{action} command failed: Actual value {ret[1]} does not match expected value {expected_value}"
                    logger.error(error_msg)
                    results.append((False, error_msg))
                    # continue
                    break
                
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

# 单例模式
plc_controller = PLCController() 