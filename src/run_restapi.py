from api.routes import api_app
from config.settings import API_CONFIG
import webbrowser
import threading

from config.version import API_VERSION

if __name__ == '__main__':
    print(f"API_VERSION: {API_VERSION}")
    def open_browser():
        import time
        time.sleep(1)  # 等待服务启动
        host = API_CONFIG["host"]
        port = API_CONFIG["port"]
        if host == '0.0.0.0':
            host = '127.0.0.1'
        url = f"http://{host}:{port}/action_control"
        url2 = f"http://{host}:{port}/action_status"
        webbrowser.open(url)
        webbrowser.open(url2)
    threading.Thread(target=open_browser, daemon=True).start()
    api_app.run(host=API_CONFIG["host"], port=API_CONFIG["port"], debug=API_CONFIG["debug"]) 