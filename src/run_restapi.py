from api.routes import api_app
from config.settings import API_CONFIG

from config.version import API_VERSION

class BrowserManager:
    """浏览器页面管理器"""
    
    def __init__(self):
        self.opened_urls = []
        self.host = API_CONFIG["host"]
        self.port = API_CONFIG["port"]
        if self.host == '0.0.0.0':
            self.host = '127.0.0.1'
   

if __name__ == '__main__':
    print(f"API_VERSION: {API_VERSION}")
    print("Starting API server...")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # 启动API服务
        api_app.run(host=API_CONFIG["host"], port=API_CONFIG["port"], debug=API_CONFIG["debug"])
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, shutting down...")
    except Exception as e:
        print(f"Error running API server: {e}")