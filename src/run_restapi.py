from api.routes import api_app
from config.settings import API_CONFIG
import webbrowser
import threading
import signal
import sys
import os
import subprocess
import platform
import time

from config.version import API_VERSION

class BrowserManager:
    """浏览器页面管理器"""
    
    def __init__(self):
        self.opened_urls = []
        self.host = API_CONFIG["host"]
        self.port = API_CONFIG["port"]
        if self.host == '0.0.0.0':
            self.host = '127.0.0.1'
    
    def open_pages(self):
        """打开所有页面"""
        urls = [
            f"http://{self.host}:{self.port}/action_control",
            f"http://{self.host}:{self.port}/action_status",
            f"http://{self.host}:{self.port}/action_setting",
            f"http://{self.host}:{self.port}/io_setting",
            f"http://{self.host}:{self.port}/doc"
        ]
        
        print("Opening browser pages...")
        for url in urls:
            try:
                # 记录打开的URL
                self.opened_urls.append(url)
                
                # 使用webbrowser模块打开页面
                webbrowser.open(url)
                print(f"  ✓ Opened: {url}")
                
                # 添加小延迟，避免浏览器被阻塞
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  ✗ Failed to open {url}: {e}")
        
        print(f"Opened {len(self.opened_urls)} pages successfully")
    
    def close_pages(self):
        """关闭所有打开的页面"""
        print("\n" + "="*50)
        print("API Server is shutting down...")
        print("="*50)
        
        # 显示打开的URL列表
        if self.opened_urls:
            print("\nOpened pages that you may want to close:")
            for i, url in enumerate(self.opened_urls, 1):
                print(f"  {i}. {url}")
            
            print("\nOptions:")
            print("  1. Manually close the browser tabs")
            print("  2. Close all browser windows (aggressive)")
            
            try:
                choice = input("\nEnter your choice (1 or 2, default 1): ").strip()
                if choice == "2":
                    self._force_close_browser()
                else:
                    print("Please manually close the browser tabs when done.")
            except (KeyboardInterrupt, EOFError):
                print("\nPlease manually close the browser tabs when done.")
        else:
            print("No browser pages were opened.")
    
    def _force_close_browser(self):
        """强制关闭浏览器（谨慎使用）"""
        print("Force closing browser...")
        
        try:
            if platform.system() == "Windows":
                # Windows: 关闭Chrome和Edge
                subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                             capture_output=True, check=False)
                subprocess.run(['taskkill', '/f', '/im', 'msedge.exe'], 
                             capture_output=True, check=False)
                print("Closed Chrome and Edge browsers")
                
            elif platform.system() == "Darwin":  # macOS
                # macOS: 关闭Chrome和Safari
                subprocess.run(['pkill', '-f', 'Google Chrome'], 
                             capture_output=True, check=False)
                subprocess.run(['pkill', '-f', 'Safari'], 
                             capture_output=True, check=False)
                print("Closed Chrome and Safari browsers")
                
            else:  # Linux
                # Linux: 关闭Chrome和Firefox
                subprocess.run(['pkill', '-f', 'chrome'], 
                             capture_output=True, check=False)
                subprocess.run(['pkill', '-f', 'firefox'], 
                             capture_output=True, check=False)
                print("Closed Chrome and Firefox browsers")
                
        except Exception as e:
            print(f"Error force closing browser: {e}")

# 全局浏览器管理器
browser_manager = BrowserManager()

def signal_handler(signum, frame):
    """信号处理器，用于优雅关闭"""
    print(f"\nReceived signal {signum}, shutting down gracefully...")
    browser_manager.close_pages()
    sys.exit(0)

def open_browser_delayed():
    """延迟打开浏览器"""
    time.sleep(1)  # 等待服务启动
    browser_manager.open_pages()

if __name__ == '__main__':
    print(f"API_VERSION: {API_VERSION}")
    print("Starting API server...")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # 终止信号
    
    # 启动浏览器线程
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    try:
        # 启动API服务
        api_app.run(host=API_CONFIG["host"], port=API_CONFIG["port"], debug=API_CONFIG["debug"])
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, shutting down...")
    except Exception as e:
        print(f"Error running API server: {e}")
    finally:
        # 确保在程序结束时关闭浏览器页面
        browser_manager.close_pages() 