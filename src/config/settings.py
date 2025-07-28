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
    BASE_DIR = os.path.join(BASE_DIR, '..')

# 静态文件路径
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'static'))
# 配置文件路径
CONFIG_PATH = os.path.join(STATIC_DIR, 'config.json')

print(f"BASE_DIR: {BASE_DIR}")
print(f"STATIC_DIR: {STATIC_DIR}")
print(f"CONFIG_PATH: {CONFIG_PATH}")

# 读取配置
with open(CONFIG_PATH, encoding='utf-8') as f:
    _config = json.load(f)

PLC_CONFIG = _config.get('PLC_CONFIG', {})
API_CONFIG = _config.get('API_CONFIG', {})
LOGGING_CONFIG = _config.get('LOGGING_CONFIG', {})
UI_CONFIG = _config.get('UI_CONFIG', {})
IO_SETTING_FILE_PATH = os.path.join(BASE_DIR, _config.get('IO_SETTING_FILE_PATH', {}))
ACTION_SETTING_FILE_PATH = os.path.join(BASE_DIR, _config.get('ACTION_SETTING_FILE_PATH', {}))
IO_TYPE_FILE_PATH = os.path.join(BASE_DIR, _config.get('IO_TYPE_FILE_PATH', {}))

hw_rev = _config.get('hw_rev','1.0.0')
plc_firmware = _config.get('plc_firmware','1.0.0')

