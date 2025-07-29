"""
日志工具模块 - 提供统一的日志记录功能
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import LOGGING_CONFIG

from config.settings import BASE_DIR


# 确保日志目录存在
log_file_path = os.path.join(BASE_DIR, LOGGING_CONFIG["log_file"])
log_dir = os.path.dirname(log_file_path)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logger = logging.getLogger("bm_control")
logger.setLevel(getattr(logging, LOGGING_CONFIG["log_level"]))

# 防止日志重复：如果已经有处理器，则不再添加
if not logger.handlers:
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOGGING_CONFIG["log_level"]))
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=LOGGING_CONFIG["max_log_size"],
        backupCount=LOGGING_CONFIG["backup_count"]
    )
    file_handler.setLevel(getattr(logging, LOGGING_CONFIG["log_level"]))
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # 防止日志传递给父logger
    logger.propagate = False

# 日志类型常量
INFO = 0
WARNING = 1
ERROR = 2

def log(log_type, message):
    """
    记录日志的函数，兼容现有代码的调用方式
    
    Args:
        log_type: 日志类型 (0=INFO, 1=WARNING, 2=ERROR)
        message: 日志消息
    """
    if log_type == INFO:
        logger.info(message)
    elif log_type == WARNING:
        logger.warning(message)
    elif log_type == ERROR:
        logger.error(message)
    else:
        logger.debug(message) 