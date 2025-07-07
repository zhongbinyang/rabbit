"""
配置文件 - 包含应用程序设置和配置参数
"""

# PLC 配置
PLC_CONFIG = {
    "host": "192.168.1.11",
    "port": 502,
    "timeout": 3.0,
    "retry_attempts": 3
}

# API 服务配置
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5001,
    "debug": False
}

# 日志配置
LOGGING_CONFIG = {
    "log_level": "INFO",
    "log_file": "Log/application.log",
    "max_log_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# UI 配置
UI_CONFIG = {
    "window_title": "BM Control System",
    "default_theme": "light",
    "font_family": "Microsoft YaHei UI",
    "font_size": 10
} 