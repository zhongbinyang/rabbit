"""
配置文件 - 包含应用程序设置和配置参数
"""

import json
import os
import sys

# 获取当前文件所在目录路径
if hasattr(sys, '_MEIPASS'):
    # PyInstaller 打包后运行时
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 源码运行时
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 配置文件路径
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'static/config.json')

# 读取配置
with open(CONFIG_PATH, encoding='utf-8') as f:
    _config = json.load(f)

PLC_CONFIG = _config.get('PLC_CONFIG', {})
API_CONFIG = _config.get('API_CONFIG', {})
LOGGING_CONFIG = _config.get('LOGGING_CONFIG', {})
UI_CONFIG = _config.get('UI_CONFIG', {})


PLC_IO_LIST_A01_GROUPED_PATH = os.path.join(BASE_DIR, '..', 'static/PLC_IO_List_A01_grouped.json')

# # PLC 配置
# PLC_CONFIG = {
#     "host": "192.168.1.11",
#     "port": 502,
#     "timeout": 3.0,
#     "retry_attempts": 3
# }

# # API 服务配置
# API_CONFIG = {
#     "host": "0.0.0.0",
#     "port": 5001,
#     "debug": False
# }

# # 日志配置
# LOGGING_CONFIG = {
#     "log_level": "INFO",
#     "log_file": "Log/application.log",
#     "max_log_size": 10 * 1024 * 1024,  # 10MB
#     "backup_count": 5
# }

# # UI 配置
# UI_CONFIG = {
#     "window_title": "BM Control System",
#     "default_theme": "light",
#     "font_family": "Microsoft YaHei UI",
#     "font_size": 10
# } 