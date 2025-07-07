import os
import datetime
import time
from collections import OrderedDict

from flask import Flask, render_template, session, request, copy_current_request_context, jsonify, send_from_directory, Blueprint, Response

import json
from flask_cors import CORS
from config.version import *
from typing import Dict, Any
from config.settings import API_CONFIG
from utils.logger import logger
from core.plc_controller import plc_controller


# 自定义API异常类
class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# 获取当前文件所在目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建API应用
api_app = Flask(__name__, 
                template_folder=os.path.join(current_dir, 'templates'))
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
    return send_from_directory('static', 'testapi.html')

@plc_api.route('/setting')
def serve_plc_io_list_manager():
    return send_from_directory('static', 'PLC_IO_List_Manager.html')

@plc_api.route('/control')
def serve_bm_ui():
    return send_from_directory('static', 'BM_UI.html')

@plc_api.route('/')
def api_documentation():
    """API文档页面"""
    # 构建API文档的结构化数据
    api_endpoints = [
        {
            'URL': 'http://{host}:5000/PLC/Control/ConnectPLC',
            'function': 'ConnectPLC',
            'description': 'Connect PLC with host and port,default host 192.168.1.11,default port 502',
            'params': '[str,int],Host,Port',
            'return': 'Result:True or False,Message:Connect message or error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ConnectPLC?Host=192.168.1.11&Port=502',
            'response': '{"Function":"ConnectPLC","Message":"Connect PLC Successful 192.168.1.11:502","Result":true,"timestamp":"2025-01-25 13:41:27_396084"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/execute_command',
            'function': 'execute_plc_command',
            'description': 'Execute PLC command with action parameter',
            'params': 'action',
            'return': 'Result:True or False,Message:Command result or error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/execute_command?action=sample_action',
            'response': '{"Function":"execute_plc_command","Message":"sample_action command successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/DisconnectPLC',
            'function': 'DisconnectPLC',
            'description': 'Disconnect PLC',
            'params': '',
            'return': 'Result:True or False,Message:Disconnect message or error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/DisconnectPLC',
            'response': '{"Function":"DisconnectPLC","Message":"Close Successful","Result":true,"timestamp":"2025-01-25 13:43:47_847322"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/LifterUp',
            'function': 'LifterUp',
            'description': 'Control Lifter Up,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Lifter Up Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/LifterUp',
            'response': '{"Function":"LifterUp","Message":"Set Lifter Up Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/LifterDown',
            'function': 'LifterDown',
            'description': 'Control Lifter Down,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Lifter Down Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/LifterDown',
            'response': '{"Function":"LifterDown","Message":"Set Lifter Down Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/ClampX_Out',
            'function': 'ClampX_Out',
            'description': 'Control Clamp X Out,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp X Out Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ClampX_Out',
            'response': '{"Function":"ClampX_Out","Message":"Set Clamp X Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/ClampX_In',
            'function': 'ClampX_In',
            'description': 'Control Clamp X In,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp X In Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ClampX_In',
            'response': '{"Function":"ClampX_In","Message":"Set Clamp X In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/ClampY_Out',
            'function': 'ClampY_Out',
            'description': 'Control Clamp Y Out,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set ClampY_Out Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ClampY_Out',
            'response': '{"Function":"ClampY_Out","Message":"Set Clamp Y Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/ClampY_In',
            'function': 'ClampY_In',
            'description': 'Control Clamp Y In,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp Y In Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ClampY_In',
            'response': '{"Function":"ClampY_In","Message":"Set Clamp Y In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/PowerOut',
            'function': 'PowerOut',
            'description': 'Control Power Out,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Power Out Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/PowerOut',
            'response': '{"Function":"PowerOut","Message":"Set Power Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/PowerIn',
            'function': 'PowerIn',
            'description': 'Control Power In,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Power In Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/PowerIn',
            'response': '{"Function":"PowerIn","Message":"Set Power In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/CommOut',
            'function': 'CommOut',
            'description': 'Control Comm Out,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Comm Out Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/CommOut',
            'response': '{"Function":"CommOut","Message":"Set Comm Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/CommIn',
            'function': 'CommIn',
            'description': 'Control Comm In,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Comm In Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/CommIn',
            'response': '{"Function":"CommIn","Message":"Set Comm In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/ResetOut',
            'function': 'ResetOut',
            'description': 'Control Reset Out,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Reset Out Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ResetOut',
            'response': '{"Function":"ResetOut","Message":"Set Reset Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/ResetIn',
            'function': 'ResetIn',
            'description': 'Control Reset In Work,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set Reset In Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/ResetIn',
            'response': '{"Function":"ResetIn","Message":"Set Reset In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/LANE_SELECT_Out',
            'function': 'LANE_SELECT_Out',
            'description': 'Control LANE_SELECT_Out,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set LANE_SELECT_Out Successful or Error message',
            'example': 'http://127.0.0.1:49900/PLC/Control/LANE_SELECT_Out',
            'response': '{"Function":"LANE_SELECT_Out","Message":"Set LANE_SELECT_Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/LANE_SELECT_In',
            'function': 'LANE_SELECT_In',
            'description': 'Control LANE_SELECT_In,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set LANE_SELECT_In Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/LANE_SELECT_In',
            'response': '{"Function":"LANE_SELECT_In","Message":"Set LANE_SELECT_In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/CRADLE_INSERT',
            'function': 'CRADLE_INSERT',
            'description': 'Control CRADLE_INSERT,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set CRADLE_INSERT Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/CRADLE_INSERT',
            'response': '{"Function":"CRADLE_INSERT","Message":"Set CRADLE_INSERT Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5000/PLC/Control/CRADLE_EXTRACT',
            'function': 'CRADLE_EXTRACT',
            'description': 'Control CRADLE EXTRACT,if normal then Result is True,Message return Control Successful',
            'params': '',
            'return': 'Result:True or False,Message:Set CRADLE EXTRACT Successful or Error message',
            'example': 'http://127.0.0.1:5000/PLC/Control/CRADLE_EXTRACT',
            'response': '{"Function":"CRADLE_EXTRACT","Message":"Set CRADLE EXTRACT Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
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
        return render_template('api_documentation.html', 
                               api_version=API_VERSION,
                               title='PLC Control API Documentation',
                               endpoints=api_endpoints)



@plc_api.route('/PLC/Control/ConnectPLC', methods=['GET', 'POST'])
def connect_plc():
    """连接PLC设备"""
    host = request.args.get('Host', type=str, default=API_CONFIG.get('host', '192.168.1.11'))
    port = request.args.get('Port', type=int, default=API_CONFIG.get('port', 502))
    
    logger.info(f"API request: Connect PLC {host}:{port}")
    ret = plc_controller.connect_plc(host, port)
    
    return jsonify(create_response("ConnectPLC", ret[0], ret[1]))


@plc_api.route('/PLC/Control/DisconnectPLC', methods=['GET', 'POST'])
def disconnect_plc():
    """断开PLC连接"""
    logger.info("API request: Disconnect PLC")
    ret = plc_controller.disconnect_plc()
    
    return jsonify(create_response("DisconnectPLC", ret[0], ret[1]))



@plc_api.route('/PLC/Control/execute_command', methods=['GET', 'POST'])
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


@plc_api.route('/PLC/Control/LifterUp', methods=['GET', 'POST'])
def lifter_up():
    """升降台上升命令"""
    logger.info("API request: Lifter up")
    ret = plc_controller.lifter_up()
    
    return jsonify(create_response("LifterUp", ret[0], ret[1]))


@plc_api.route('/PLC/Control/LifterDown', methods=['GET', 'POST'])
def lifter_down():
    """升降台下降命令"""
    logger.info("API request: Lifter down")
    ret = plc_controller.lifter_down()
    
    return jsonify(create_response("LifterDown", ret[0], ret[1]))


@plc_api.route('/PLC/Control/ClampX_Out', methods=['GET', 'POST'])
def clamp_x_out():
    """X轴夹钳伸出命令"""
    logger.info("API request: Clamp x out")
    ret = plc_controller.clamp_x_out()
    
    return jsonify(create_response("ClampX_Out", ret[0], ret[1]))


@plc_api.route('/PLC/Control/ClampX_In', methods=['GET', 'POST'])
def clamp_x_in():
    """X轴夹钳收回命令"""
    logger.info("API request: Clamp x in")
    ret = plc_controller.clamp_x_in()
    
    return jsonify(create_response("ClampX_In", ret[0], ret[1]))


@plc_api.route('/PLC/Control/ClampY_Out', methods=['GET', 'POST'])
def clamp_y_out():
    """Y轴夹钳伸出命令"""
    logger.info("API request: Clamp y out")
    ret = plc_controller.clamp_y_out()
    
    return jsonify(create_response("ClampY_Out", ret[0], ret[1]))


@plc_api.route('/PLC/Control/ClampY_In', methods=['GET', 'POST'])
def clamp_y_in():
    """Y轴夹钳收回命令"""
    logger.info("API request: Clamp y in")
    ret = plc_controller.clamp_y_in()
    
    return jsonify(create_response("ClampY_In", ret[0], ret[1]))


@plc_api.route('/PLC/Control/PowerOut', methods=['GET', 'POST'])
def power_out():
    """电源拔出命令"""
    logger.info("API request: Power out")
    ret = plc_controller.power_out()
    
    return jsonify(create_response("PowerOut", ret[0], ret[1]))


@plc_api.route('/PLC/Control/PowerIn', methods=['GET', 'POST'])
def power_in():
    """电源插入命令"""
    logger.info("API request: Power in")
    ret = plc_controller.power_in()
    
    return jsonify(create_response("PowerIn", ret[0], ret[1]))


@plc_api.route('/PLC/Control/CommOut', methods=['GET', 'POST'])
def comm_out():
    """通信口拔出命令"""
    logger.info("API request: Comm out")
    ret = plc_controller.comm_out()
    
    return jsonify(create_response("CommOut", ret[0], ret[1]))


@plc_api.route('/PLC/Control/CommIn', methods=['GET', 'POST'])
def comm_in():
    """通信口插入命令"""
    logger.info("API request: Comm in")
    ret = plc_controller.comm_in()
    
    return jsonify(create_response("CommIn", ret[0], ret[1]))


@plc_api.route('/PLC/Control/ResetOut', methods=['GET', 'POST'])
def reset_out():
    """重置按钮释放命令"""
    logger.info("API request: Reset out")
    ret = plc_controller.reset_off()
    
    return jsonify(create_response("ResetOut", ret[0], ret[1]))


@plc_api.route('/PLC/Control/ResetIn', methods=['GET', 'POST'])
def reset_in():
    """重置按钮按下命令"""
    logger.info("API request: Reset in")
    ret = plc_controller.reset_on()
    
    return jsonify(create_response("ResetIn", ret[0], ret[1]))


@plc_api.route('/PLC/Control/LANE_SELECT_Out', methods=['GET', 'POST'])
def lane_out():
    """通道选择释放命令"""
    logger.info("API request: Lane select out")
    ret = plc_controller.lane_select_off()
    
    return jsonify(create_response("LANE_SELECT_Out", ret[0], ret[1]))


@plc_api.route('/PLC/Control/LANE_SELECT_In', methods=['GET', 'POST'])
def lane_in():
    """通道选择按下命令"""
    logger.info("API request: Lane select in")
    ret = plc_controller.lane_select_on()
    
    return jsonify(create_response("LANE_SELECT_In", ret[0], ret[1]))


@plc_api.route('/PLC/Control/CRADLE_INSERT', methods=['GET', 'POST'])
def cradle_insert():
    """托架插入命令"""
    logger.info("API request: Cradle insert")
    ret = plc_controller.cradle_inserted()
    
    return jsonify(create_response("CRADLE_INSERT", ret[0], ret[1]))


@plc_api.route('/PLC/Control/CRADLE_EXTRACT', methods=['GET', 'POST'])
def cradle_extract():
    """托架拔出命令"""
    logger.info("API request: Cradle extract")
    ret = plc_controller.cradle_extracted()
    
    return jsonify(create_response("CRADLE_EXTRACT", ret[0], ret[1]))


@plc_api.route('/PLC/Status/GetCradleState', methods=['GET', 'POST'])
def get_cradle_state():
    """获取托架状态"""
    logger.info("API request: Get cradle state")
    ret = plc_controller.get_cradle_state()
    
    if ret[0]:
        state = "插入" if ret[1] == 1 else "拔出"
        return jsonify(create_response("GetCradleState", ret[0], f"Cradle state: {state} ({ret[1]})"))
    else:
        return jsonify(create_response("GetCradleState", ret[0], "Get cradle state failed"))


@plc_api.route('/PLC/Status/GetFirmware', methods=['GET', 'POST'])
def get_firmware():
    """获取固件版本"""
    logger.info("API request: Get firmware")
    ret = plc_controller.get_plc_firmware()
    
    if ret[0]:
        return jsonify(create_response("GetFirmware", ret[0], f"Firmware version: {ret[1]}"))
    else:
        return jsonify(create_response("GetFirmware", ret[0], "Get firmware failed"))


@plc_api.route('/get_version', methods=['GET', 'POST'])
def get_version():
    """获取系统版本"""
    logger.info("API request: Get version")
    version = {
        "name": "BM Control System",
        "version": "2.0.0",
        "build_date": "2025-06-30",
        "description": "PLC control system"
    }
    
    return jsonify(create_response("GetVersion", True, json.dumps(version)))

@plc_api.route('/get_api_version', methods=['GET', 'POST'])
def get_api_version():
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
        file_path = os.path.join(current_dir, 'static', filename)
        logger.info(f"Writing JSON to file: {file_path}")
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        return jsonify(create_response("write_json_file", True, f"Successfully wrote to {filename}")), 200
    except Exception as e:
        logger.error(f"Error writing JSON file: {str(e)}")
        return jsonify(create_response("write_json_file", False, f"Error writing file: {str(e)}")), 500


@plc_api.route('/api/read_json_file', methods=['GET', 'POST'])
def read_json_file():
    """从static目录读取JSON文件"""
    # 支持GET和POST方法
    if request.method == 'POST' and request.is_json:
        filename = request.json.get('filename')
    else:
        filename = request.args.get('filename')
    
    if not filename:
        return jsonify(create_response("read_json_file", False, "Missing required parameter: filename")), 400
    
    # 安全检查：确保文件名是安全的（不包含路径遍历）
    if '..' in filename or filename.startswith('/'):
        return jsonify(create_response("read_json_file", False, "Invalid filename")), 400
    
    # 确保文件扩展名是.json
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        # 构建完整的文件路径
        file_path = os.path.join(current_dir, 'static', filename)
        logger.info(f"Reading JSON from file: {file_path}")
        
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 直接返回JSON内容，而不是包装在content字段中
        # 这样前端可以直接访问数据
        return jsonify(content), 200
    except FileNotFoundError:
        return jsonify(create_response("read_json_file", False, f"File not found: {filename}")), 404
    except json.JSONDecodeError:
        return jsonify(create_response("read_json_file", False, f"Invalid JSON in file: {filename}")), 400
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        return jsonify(create_response("read_json_file", False, f"Error reading file: {str(e)}")), 500

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

