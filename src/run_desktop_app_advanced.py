import webview
import threading
import time
import sys
import os
from api.routes import api_app
from config.settings import API_CONFIG
from config.version import API_VERSION

# Windows特定的无控制台设置
if sys.platform.startswith('win'):
    import ctypes
    import subprocess
    
    # 隐藏控制台窗口
    def hide_console():
        """隐藏控制台窗口"""
        try:
            # 获取当前进程句柄
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            
            # 隐藏控制台窗口
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
        except:
            pass
    
    # 重定向标准输出和错误输出
    def redirect_output():
        """重定向输出到空设备"""
        try:
            # 重定向到NUL设备
            null_device = open(os.devnull, 'w')
            sys.stdout = null_device
            sys.stderr = null_device
        except:
            pass

class AdvancedDesktopApp:
    def __init__(self, silent=True):
        self.host = API_CONFIG["host"]
        self.port = API_CONFIG["port"]
        self.debug = False
        self.windows = {}
        self.api_thread = None
        self.silent = True  # 静默模式，不输出日志
        
        # Windows无控制台设置
        if sys.platform.startswith('win') and silent:
            hide_console()
            redirect_output()
        
        # 如果host是0.0.0.0，转换为127.0.0.1用于本地访问
        if self.host == '0.0.0.0':
            self.host = '127.0.0.1'
    
    def log(self, message):
        """条件性日志输出"""
        if not self.silent:
            print(message)
    
    def start_api_server(self):
        """在后台启动API服务器"""
        try:
            self.log(f"Starting API server on {self.host}:{self.port}")
            
            # Windows下静默启动Flask
            if sys.platform.startswith('win') and self.silent:
                # 重定向Flask的输出
                import io
                import contextlib
                
                # 临时重定向输出
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    api_app.run(host=API_CONFIG["host"], port=API_CONFIG["port"], debug=False, use_reloader=False)
            else:
                api_app.run(host=API_CONFIG["host"], port=API_CONFIG["port"], debug=False, use_reloader=False)
                
        except Exception as e:
            if not self.silent:
                print(f"API server error: {e}")
    
    def wait_for_server(self, timeout=10):
        """等待服务器启动"""
        import requests
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://{self.host}:{self.port}/health", timeout=1)
                if response.status_code == 200:
                    self.log("API server is ready")
                    return True
            except:
                time.sleep(0.5)
        return False
    
    def create_control_window(self):
        """创建Action Control窗口"""
        control_url = f"http://{self.host}:{self.port}/action_control"
        window = webview.create_window(
            title='Action Control - Tester Control System',
            url=control_url,
            width=1400,
            height=900,
            resizable=True,
            text_select=True,
            confirm_close=False,
            min_size=(800, 600),
            background_color='#f5f5f5',
            frameless=False,
            easy_drag=True,
            on_top=False
        )
        return window
    
    def create_status_window(self):
        """创建Action Status窗口"""
        status_url = f"http://{self.host}:{self.port}/action_status"
        window = webview.create_window(
            title='Action Status - Tester Control System',
            url=status_url,
            width=1200,
            height=700,
            resizable=True,
            text_select=True,
            confirm_close=False,
            min_size=(600, 400),
            background_color='#f5f5f5',
            frameless=False,
            easy_drag=True,
            on_top=False
        )
        return window
    
    def create_io_setting_window(self):
        """创建IO Setting窗口"""
        io_setting_url = f"http://{self.host}:{self.port}/io_setting"
        window = webview.create_window(
            title='IO Setting - Tester Control System',
            url=io_setting_url,
            width=1200,
            height=800,
            resizable=True,
            text_select=True,
            confirm_close=False,
            min_size=(800, 600),
            background_color='#f5f5f5',
            frameless=False,
            easy_drag=True,
            on_top=False
        )
        return window
    
    def create_action_setting_window(self):
        """创建Action Setting窗口"""
        action_setting_url = f"http://{self.host}:{self.port}/action_setting"
        window = webview.create_window(
            title='Action Setting - Tester Control System',
            url=action_setting_url,
            width=1200,
            height=800,
            resizable=True,
            text_select=True,
            confirm_close=False,
            min_size=(800, 600),
            background_color='#f5f5f5',
            frameless=False,
            easy_drag=True,
            on_top=False
        )
        return window
    
    def create_doc_window(self):
        """创建Documentation窗口"""
        doc_url = f"http://{self.host}:{self.port}/doc"
        window = webview.create_window(
            title='Documentation - Tester Control System',
            url=doc_url,
            width=1400,
            height=900,
            resizable=True,
            text_select=True,
            confirm_close=False,
            min_size=(1000, 700),
            background_color='#f5f5f5',
            frameless=False,
            easy_drag=True,
            on_top=False
        )
        return window
    
    def create_single_window(self):
        """创建单个窗口，包含所有页面的标签页"""
        # 创建一个包含所有页面的HTML页面
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tester Control System</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background-color: #2c3e50;
                    color: white;
                    padding: 10px 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .tab-container {{
                    display: flex;
                    background-color: #34495e;
                    overflow-x: auto;
                }}
                .tab {{
                    padding: 10px 20px;
                    background-color: #34495e;
                    color: white;
                    cursor: pointer;
                    border: none;
                    white-space: nowrap;
                    transition: background-color 0.3s;
                    min-width: 120px;
                    text-align: center;
                }}
                .tab.active {{
                    background-color: #2c3e50;
                }}
                .tab:hover {{
                    background-color: #2c3e50;
                }}
                .content {{
                    height: calc(100vh - 80px);
                }}
                .iframe {{
                    width: 100%;
                    height: 100%;
                    border: none;
                    display: none;
                }}
                .iframe.active {{
                    display: block;
                }}
                .status-indicator {{
                    display: inline-block;
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    margin-right: 8px;
                    background-color: #27ae60;
                }}
                .status-indicator.disconnected {{
                    background-color: #e74c3c;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Tester Control System v{API_VERSION}</h2>
                <div>
                    <span class="status-indicator" id="status-indicator"></span>
                    <span id="status">Connected</span>
                </div>
            </div>
            <div class="tab-container">
                <button class="tab active" onclick="showTab('control')">Action Control</button>
                <button class="tab" onclick="showTab('status')">Action Status</button>
                <button class="tab" onclick="showTab('io_setting')">IO Setting</button>
                <button class="tab" onclick="showTab('action_setting')">Action Setting</button>
                <button class="tab" onclick="showTab('doc')">Documentation</button>
            </div>
            <div class="content">
                <iframe id="control-frame" class="iframe active" src="http://{self.host}:{self.port}/action_control"></iframe>
                <iframe id="status-frame" class="iframe" src="http://{self.host}:{self.port}/action_status"></iframe>
                <iframe id="io_setting-frame" class="iframe" src="http://{self.host}:{self.port}/io_setting"></iframe>
                <iframe id="action_setting-frame" class="iframe" src="http://{self.host}:{self.port}/action_setting"></iframe>
                <iframe id="doc-frame" class="iframe" src="http://{self.host}:{self.port}/doc"></iframe>
            </div>
            <script>
                function showTab(tabName) {{
                    // 隐藏所有iframe
                    document.querySelectorAll('.iframe').forEach(iframe => {{
                        iframe.classList.remove('active');
                    }});
                    
                    // 移除所有tab的active类
                    document.querySelectorAll('.tab').forEach(tab => {{
                        tab.classList.remove('active');
                    }});
                    
                    // 显示选中的iframe
                    document.getElementById(tabName + '-frame').classList.add('active');
                    
                    // 添加active类到选中的tab
                    event.target.classList.add('active');
                }}
                
                // 定期检查连接状态
                setInterval(() => {{
                    fetch('http://{self.host}:{self.port}/health')
                        .then(response => {{
                            document.getElementById('status').textContent = 'Connected';
                            document.getElementById('status-indicator').classList.remove('disconnected');
                        }})
                        .catch(() => {{
                            document.getElementById('status').textContent = 'Disconnected';
                            document.getElementById('status-indicator').classList.add('disconnected');
                        }});
                }}, 5000);
                
                // 页面加载完成后立即检查一次状态
                window.addEventListener('load', () => {{
                    fetch('http://{self.host}:{self.port}/health')
                        .then(response => {{
                            document.getElementById('status').textContent = 'Connected';
                            document.getElementById('status-indicator').classList.remove('disconnected');
                        }})
                        .catch(() => {{
                            document.getElementById('status').textContent = 'Disconnected';
                            document.getElementById('status-indicator').classList.add('disconnected');
                        }});
                }});
            </script>
        </body>
        </html>
        """
        
        # 创建临时HTML文件
        temp_html = os.path.join(os.path.dirname(__file__), 'temp_desktop_app.html')
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        window = webview.create_window(
            title='Tester Control System',
            url=temp_html,
            width=1600,
            height=1000,
            resizable=True,
            text_select=True,
            confirm_close=True,
            min_size=(1200, 800),
            background_color='#f5f5f5',
            frameless=False,
            easy_drag=True,
            on_top=False
        )
        
        # 清理临时文件
        def cleanup():
            try:
                os.remove(temp_html)
            except:
                pass
        
        return window, cleanup
    
    def run_single_window(self):
        """运行单窗口模式"""
        self.log("Starting single window mode...")
        
        # 启动API服务器
        self.api_thread = threading.Thread(target=self.start_api_server, daemon=True)
        self.api_thread.start()
        
        # 等待服务器启动
        if not self.wait_for_server():
            if not self.silent:
                print("Failed to start API server")
            return
        
        # 创建单窗口
        window, cleanup = self.create_single_window()
        
        # 启动webview
        try:
            webview.start(debug=self.debug)
        finally:
            cleanup()
    
    def run(self, mode='single'):
        """运行桌面应用"""
        if not self.silent:
            print(f"API_VERSION: {API_VERSION}")
            print("Starting desktop application...")
        
        self.run_single_window()

def main():
    """主函数"""
    try:
        # 检查命令行参数
        mode = 'multi'
        silent = True
        
        app = AdvancedDesktopApp(silent=silent)
        app.run(mode)
        
    except KeyboardInterrupt:
        if not silent:
            print("\nApplication stopped by user")
    except Exception as e:
        if not silent:
            print(f"Error starting application: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main() 