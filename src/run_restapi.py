from api.routes import api_app
from config.settings import API_CONFIG

if __name__ == '__main__':
    api_app.run(host=API_CONFIG["host"], port=API_CONFIG["port"], debug=API_CONFIG["debug"]) 