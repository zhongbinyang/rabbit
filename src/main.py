#!flask/bin/python
import sys
import threading
import time
import socket
from PyQt5 import QtWidgets
from api.routes import api_app
from ui.app import *
from ui.app import UIApplication
from config.settings import API_CONFIG

def is_port_in_use(port, host='0.0.0.0'):
    """检查指定端口是否已被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True


if __name__ == '__main__':
    api_port = API_CONFIG["port"]
    api_host = API_CONFIG["host"]
    
    # 检查API端口是否已被占用
    if is_port_in_use(api_port, api_host):
        print(f"API服务已在端口 {api_port} 运行，跳过API启动")
    else:
        print(f"启动API服务于 {api_host}:{api_port}")
        thread = threading.Thread(target=lambda: api_app.run(api_host, api_port, debug=API_CONFIG.get("debug", False)))
        thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        thread.start()
        time.sleep(1)  # 等待API启动
    
    # 启动UI
    UIApplication.run()
