import os
import datetime
import sys

from flask import Flask, render_template, session, request, copy_current_request_context, jsonify, send_from_directory, Blueprint, Response

import json
from config.version import *
from typing import Dict, Any
from config.settings import API_CONFIG, PLC_CONFIG
from utils.logger import logger
from core.plc_controller import plc_controller
from config.settings import BASE_DIR, STATIC_DIR


# 自定义API异常类
class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# 创建API应用
api_app = Flask(__name__, static_folder=STATIC_DIR, template_folder=STATIC_DIR)
api_app.config['JSON_SORT_KEYS'] = False

# 创建蓝图
plc_api = Blueprint('plc_api', __name__)

def create_response(function: str, result: bool, message: str) -> Dict[str, Any]:
    """
    创建标准API响应
    
    Args:
        function: 函数名称
        result: 操作结果
        message: 消息内容
        
    Returns:
        标准格式的响应字典
    """
    return {
        'Function': function,
        'Result': result,
        'Message': message,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S_%f")
    }

@plc_api.route('/test')
def serve_testapi():
    return send_from_directory(STATIC_DIR, 'testapi.html')

@plc_api.route('/io_setting')
def serve_plc_io_list_manager():
    return send_from_directory(STATIC_DIR, 'io_setting.html')

@plc_api.route('/action_setting')
def serve_plc_action_list_manager():
    return send_from_directory(STATIC_DIR, 'action_setting.html')

@plc_api.route('/action_control')
def serve_bm_ui():
    return send_from_directory(STATIC_DIR, 'action_control.html')

@plc_api.route('/action_status')
def serve_action_status():
    return send_from_directory(STATIC_DIR, 'action_status.html')

@plc_api.route('/')
def api_documentation():
    """API文档页面"""
    # 构建API文档的结构化数据
    api_endpoints = [
        {
            'URL': 'http://{host}:5001/connect_plc',
            'function': 'connect_plc',
            'description': 'Connect PLC with host and port, default host 192.168.1.11, default port 502',
            'params': '[str,int],Host,Port',
            'return': 'Result:True or False,Message:Connect message or error message',
            'example': 'http://127.0.0.1:5001/connect_plc?Host=192.168.1.11&Port=502',
            'response': '{"Function":"ConnectPLC","Message":"Connect PLC Successful 192.168.1.11:502","Result":true,"timestamp":"2025-01-25 13:41:27_396084"}'
        },
        {
            'URL': 'http://{host}:5001/execute_command',
            'function': 'execute_plc_command',
            'description': 'Execute PLC command with action parameter',
            'params': 'action',
            'return': 'Result:True or False,Message:Command result or error message',
            'example': 'http://127.0.0.1:5001/execute_command?action=sample_action',
            'response': '{"Function":"execute_plc_command","Message":"sample_action command successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/disconnect_plc',
            'function': 'disconnect_plc',
            'description': 'Disconnect PLC',
            'params': '',
            'return': 'Result:True or False,Message:Disconnect message or error message',
            'example': 'http://127.0.0.1:5001/disconnect_plc',
            'response': '{"Function":"DisconnectPLC","Message":"Close Successful","Result":true,"timestamp":"2025-01-25 13:43:47_847322"}'
        }
    ]
    
    # 支持通过format=json查询参数或Accept头获取JSON格式
    if request.args.get('format') == 'json' or request.headers.get('Accept') == 'application/json':
        # 返回JSON格式的API文档
        return jsonify({
            'api_version': API_VERSION,
            'title': 'PLC Control API Documentation',
            'description': 'API documentation for PLC control system',
            'note': 'All endpoints can use POST or GET methods',
            'endpoints': api_endpoints
        })
    else:
        # 返回HTML格式的API文档
        return render_template('doc.html', 
                               api_version=API_VERSION,
                               title='PLC Control API Documentation',
                               endpoints=api_endpoints)



@plc_api.route('/connect_plc', methods=['GET', 'POST'])
def connect_plc():
    """连接PLC设备"""
    host = request.args.get('Host', type=str, default=PLC_CONFIG.get('host', '192.168.1.11'))
    port = request.args.get('Port', type=int, default=PLC_CONFIG.get('port', 502))
    
    logger.info(f"API request: Connect PLC {host}:{port}")
    ret = plc_controller.connect_plc(host, port)
    
    return jsonify(create_response("ConnectPLC", ret[0], ret[1]))


@plc_api.route('/disconnect_plc', methods=['GET', 'POST'])
def disconnect_plc():
    """断开PLC连接"""
    logger.info("API request: Disconnect PLC")
    ret = plc_controller.disconnect_plc()
    
    return jsonify(create_response("DisconnectPLC", ret[0], ret[1]))



@plc_api.route('/execute_command', methods=['GET', 'POST'])
def execute_plc_command():
    """执行PLC命令"""
    # 同时支持GET和POST请求参
    if request.method == 'POST' and request.is_json:
        action = request.get_json().get('action',  None)
    else:
        action = request.args.get('action', type=str, default=None)
    
    if not action:
        return jsonify(create_response("execute_plc_command", False, "action parameter is required")), 400
    
    logger.info(f"API request: Execute PLC command with action '{action}'")
    
    try:
        ret = plc_controller._execute_plc_command(action)
        return jsonify(create_response("execute_plc_command", ret[0], ret[1]))
    except Exception as e:
        return jsonify(create_response("execute_plc_command", False, f"Error executing command: {str(e)}")), 500


@plc_api.route('/set_control', methods=['GET', 'POST'])
def set_control():
    """设置PLC控制"""
    # 同时支持GET和POST请求参
    if request.method == 'POST' and request.is_json:
        control_name = request.get_json().get('control_name',  None)
        control_state = request.get_json().get('control_state',  None)
    else:
        control_name = request.args.get('control_name', type=str, default=None)
        control_state = request.args.get('control_state', type=str, default=None)
    
    if not control_name or not control_state:
        return jsonify(create_response("set_control", False, "control_name and control_state parameter is required")), 400
    
    logger.info(f"API request: Set PLC control with control_name '{control_name}' and control_state '{control_state}'")
    
    try:
        ret = plc_controller._set_control(control_name, control_state)

        response_data = {
            "state": control_state if ret[0] else "",
            "result": ret[0],
            "status": "" if ret[0] else ret[1]
        }

        # Return response
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        )
    except Exception as e:
        response_data = {
            "state": "",
            "result": False,
            "status": "Error setting control: " + str(e)
        }

        # Return response
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        )
    
@plc_api.route('/get_control', methods=['GET', 'POST'])
def get_control():
    """获取PLC控制"""
    # 同时支持GET和POST请求参
    if request.method == 'POST' and request.is_json:
        control_name = request.get_json().get('control_name',  None)
    else:
        control_name = request.args.get('control_name', type=str, default=None)
    
    if not control_name:
        return jsonify(create_response("set_control", False, "control_name parameter is required")), 400
    
    logger.info(f"API request: Get PLC control with control_name '{control_name}'")
    
    try:
        ret = plc_controller._get_control(control_name)
        response_data = {
            "state": ret[2],
            "result": ret[0],
            "status": "" if ret[0] else ret[1]
        }
        # Return response
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        )
    except Exception as e:
        response_data = {
            "state": ret[2],
            "result": False,
            "status": "Error getting control: " + str(e)
        }
        # Return response
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        )
    
@plc_api.route('/get_version', methods=['GET', 'POST'])
def get_version():
    return jsonify({'Function':"get_api_version",'Result': True, 'Message': API_VERSION,
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@plc_api.route('/api/write_json_file', methods=['POST'])
def write_json_file():
    """写入JSON文件到static目录"""
    if not request.is_json:
        return jsonify(create_response("write_json_file", False, "Request must be JSON")), 400
    
    data = request.json
    if not data or 'filename' not in data or 'content' not in data:
        return jsonify(create_response("write_json_file", False, "Missing required parameters: filename and content")), 400
    
    filename = data['filename']
    content = data['content']
    
    # 安全检查：确保文件名是安全的（不包含路径遍历）
    if '..' in filename or filename.startswith('/'):
        return jsonify(create_response("write_json_file", False, "Invalid filename")), 400
    
    # 确保文件扩展名是.json
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        # 构建完整的文件路径
        file_path = os.path.join(BASE_DIR, filename)
        logger.info(f"Writing JSON to file: {file_path}")
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        return jsonify(create_response("write_json_file", True, f"Successfully wrote to {filename}")), 200
    except Exception as e:
        logger.error(f"Error writing JSON file: {str(e)}")
        return jsonify(create_response("write_json_file", False, f"Error writing file: {str(e)}")), 500
# 注册蓝图
api_app.register_blueprint(plc_api)


@api_app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify(create_response("Error", False, "Resource not found")), 404


@api_app.errorhandler(500)
def internal_server_error(error):
    """处理500错误"""
    return jsonify(create_response("Error", False, "Internal server error")), 500

