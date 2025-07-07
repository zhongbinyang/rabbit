"""
异常处理模块 - 定义应用程序的自定义异常类
"""

class PLCError(Exception):
    """PLC通信或操作异常的基类"""
    pass


class PLCConnectionError(PLCError):
    """PLC连接异常"""
    pass


class PLCTimeoutError(PLCError):
    """PLC操作超时异常"""
    pass


class PLCCommandError(PLCError):
    """PLC命令执行异常"""
    pass


class ConfigError(Exception):
    """配置错误异常"""
    pass


class APIError(Exception):
    """API相关异常的基类"""
    
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def to_dict(self):
        """转换为API响应字典"""
        return {
            'error': self.message,
            'status_code': self.status_code
        }


def handle_exception(func):
    """
    装饰器：处理函数执行过程中可能出现的异常
    
    Args:
        func: 需要进行异常处理的函数
        
    Returns:
        包装后的函数
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PLCConnectionError as e:
            from utils.logger import logger
            logger.error(f"PLC Connection Error: {str(e)}")
            return False, f"PLC Connection Error: {str(e)}"
        except PLCTimeoutError as e:
            from utils.logger import logger
            logger.error(f"PLC Operation Timeout: {str(e)}")
            return False, f"PLC Operation Timeout: {str(e)}"
        except PLCCommandError as e:
            from utils.logger import logger
            logger.error(f"PLC Command Execution Error: {str(e)}")
            return False, f"PLC Command Execution Error: {str(e)}"
        except Exception as e:
            from utils.logger import logger
            logger.error(f"Unexpected Error: {str(e)}")
            return False, f"Unexpected Error: {str(e)}"
    return wrapper 