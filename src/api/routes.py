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


# 自定义API异常类
class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# 获取当前文件所在目录路径
if hasattr(sys, '_MEIPASS'):
    # PyInstaller 打包后运行时
    base_dir = os.path.dirname(sys.executable)
    static_dir = os.path.abspath(os.path.join(base_dir, 'static'))
    print(f"PyInstaller 打包后运行时: {base_dir}")
else:
    # 源码运行时
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.abspath(os.path.join(base_dir, '..', 'static'))

# 创建API应用
api_app = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
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
    return send_from_directory(static_dir, 'testapi.html')

@plc_api.route('/setting')
def serve_plc_io_list_manager():
    return send_from_directory(static_dir, 'PLC_IO_List_Manager.html')

@plc_api.route('/control')
def serve_bm_ui():
    return send_from_directory(static_dir, 'BM_UI.html')

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
        },
        {
            'URL': 'http://{host}:5001/lifter_up',
            'function': 'lifter_up',
            'description': 'Control Lifter Up',
            'params': '',
            'return': 'Result:True or False,Message:Set Lifter Up Successful or Error message',
            'example': 'http://127.0.0.1:5001/lifter_up',
            'response': '{"Function":"LifterUp","Message":"Set Lifter Up Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/lifter_down',
            'function': 'lifter_down',
            'description': 'Control Lifter Down',
            'params': '',
            'return': 'Result:True or False,Message:Set Lifter Down Successful or Error message',
            'example': 'http://127.0.0.1:5001/lifter_down',
            'response': '{"Function":"LifterDown","Message":"Set Lifter Down Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/clampx_out',
            'function': 'clamp_x_out',
            'description': 'Control Clamp X Out',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp X Out Successful or Error message',
            'example': 'http://127.0.0.1:5001/clampx_out',
            'response': '{"Function":"ClampX_Out","Message":"Set Clamp X Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/clampx_in',
            'function': 'clamp_x_in',
            'description': 'Control Clamp X In',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp X In Successful or Error message',
            'example': 'http://127.0.0.1:5001/clampx_in',
            'response': '{"Function":"ClampX_In","Message":"Set Clamp X In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/clampy_out',
            'function': 'clamp_y_out',
            'description': 'Control Clamp Y Out',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp Y Out Successful or Error message',
            'example': 'http://127.0.0.1:5001/clampy_out',
            'response': '{"Function":"ClampY_Out","Message":"Set Clamp Y Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/clampy_in',
            'function': 'clamp_y_in',
            'description': 'Control Clamp Y In',
            'params': '',
            'return': 'Result:True or False,Message:Set Clamp Y In Successful or Error message',
            'example': 'http://127.0.0.1:5001/clampy_in',
            'response': '{"Function":"ClampY_In","Message":"Set Clamp Y In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/power_out',
            'function': 'power_out',
            'description': 'Control Power Out',
            'params': '',
            'return': 'Result:True or False,Message:Set Power Out Successful or Error message',
            'example': 'http://127.0.0.1:5001/power_out',
            'response': '{"Function":"PowerOut","Message":"Set Power Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/power_in',
            'function': 'power_in',
            'description': 'Control Power In',
            'params': '',
            'return': 'Result:True or False,Message:Set Power In Successful or Error message',
            'example': 'http://127.0.0.1:5001/power_in',
            'response': '{"Function":"PowerIn","Message":"Set Power In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/comm_out',
            'function': 'comm_out',
            'description': 'Control Comm Out',
            'params': '',
            'return': 'Result:True or False,Message:Set Comm Out Successful or Error message',
            'example': 'http://127.0.0.1:5001/comm_out',
            'response': '{"Function":"CommOut","Message":"Set Comm Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/comm_in',
            'function': 'comm_in',
            'description': 'Control Comm In',
            'params': '',
            'return': 'Result:True or False,Message:Set Comm In Successful or Error message',
            'example': 'http://127.0.0.1:5001/comm_in',
            'response': '{"Function":"CommIn","Message":"Set Comm In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/reset_out',
            'function': 'reset_out',
            'description': 'Control Reset Out',
            'params': '',
            'return': 'Result:True or False,Message:Set Reset Out Successful or Error message',
            'example': 'http://127.0.0.1:5001/reset_out',
            'response': '{"Function":"ResetOut","Message":"Set Reset Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/reset_in',
            'function': 'reset_in',
            'description': 'Control Reset In',
            'params': '',
            'return': 'Result:True or False,Message:Set Reset In Successful or Error message',
            'example': 'http://127.0.0.1:5001/reset_in',
            'response': '{"Function":"ResetIn","Message":"Set Reset In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/lane_select_out',
            'function': 'lane_out',
            'description': 'Control Lane Select Out',
            'params': '',
            'return': 'Result:True or False,Message:Set Lane Select Out Successful or Error message',
            'example': 'http://127.0.0.1:5001/lane_select_out',
            'response': '{"Function":"LANE_SELECT_Out","Message":"Set LANE_SELECT_Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/lane_select_in',
            'function': 'lane_in',
            'description': 'Control Lane Select In',
            'params': '',
            'return': 'Result:True or False,Message:Set Lane Select In Successful or Error message',
            'example': 'http://127.0.0.1:5001/lane_select_in',
            'response': '{"Function":"LANE_SELECT_In","Message":"Set LANE_SELECT_In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/cradle_insert',
            'function': 'cradle_insert',
            'description': 'Control Cradle Insert',
            'params': '',
            'return': 'Result:True or False,Message:Set Cradle Insert Successful or Error message',
            'example': 'http://127.0.0.1:5001/cradle_insert',
            'response': '{"Function":"CRADLE_INSERT","Message":"Set CRADLE_INSERT Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}'
        },
        {
            'URL': 'http://{host}:5001/cradle_extract',
            'function': 'cradle_extract',
            'description': 'Control Cradle Extract',
            'params': '',
            'return': 'Result:True or False,Message:Set Cradle Extract Successful or Error message',
            'example': 'http://127.0.0.1:5001/cradle_extract',
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


@plc_api.route('/lifter_up', methods=['GET', 'POST'])
def lifter_up():
    """升降台上升命令"""
    logger.info("API request: Lifter up")
    ret = plc_controller.lifter_up()
    
    return jsonify(create_response("LifterUp", ret[0], ret[1]))


@plc_api.route('/lifter_down', methods=['GET', 'POST'])
def lifter_down():
    """升降台下降命令"""
    logger.info("API request: Lifter down")
    ret = plc_controller.lifter_down()
    
    return jsonify(create_response("LifterDown", ret[0], ret[1]))


@plc_api.route('/clampx_out', methods=['GET', 'POST'])
def clamp_x_out():
    """X轴夹钳伸出命令"""
    logger.info("API request: Clamp x out")
    ret = plc_controller.clamp_x_out()
    
    return jsonify(create_response("ClampX_Out", ret[0], ret[1]))


@plc_api.route('/clampx_in', methods=['GET', 'POST'])
def clamp_x_in():
    """X轴夹钳收回命令"""
    logger.info("API request: Clamp x in")
    ret = plc_controller.clamp_x_in()
    
    return jsonify(create_response("ClampX_In", ret[0], ret[1]))


@plc_api.route('/clampy_out', methods=['GET', 'POST'])
def clamp_y_out():
    """Y轴夹钳伸出命令"""
    logger.info("API request: Clamp y out")
    ret = plc_controller.clamp_y_out()
    
    return jsonify(create_response("ClampY_Out", ret[0], ret[1]))


@plc_api.route('/clampy_in', methods=['GET', 'POST'])
def clamp_y_in():
    """Y轴夹钳收回命令"""
    logger.info("API request: Clamp y in")
    ret = plc_controller.clamp_y_in()
    
    return jsonify(create_response("ClampY_In", ret[0], ret[1]))


@plc_api.route('/power_out', methods=['GET', 'POST'])
def power_out():
    """电源拔出命令"""
    logger.info("API request: Power out")
    ret = plc_controller.power_out()
    
    return jsonify(create_response("PowerOut", ret[0], ret[1]))


@plc_api.route('/power_in', methods=['GET', 'POST'])
def power_in():
    """电源插入命令"""
    logger.info("API request: Power in")
    ret = plc_controller.power_in()
    
    return jsonify(create_response("PowerIn", ret[0], ret[1]))


@plc_api.route('/comm_out', methods=['GET', 'POST'])
def comm_out():
    """通信口拔出命令"""
    logger.info("API request: Comm out")
    ret = plc_controller.comm_out()
    
    return jsonify(create_response("CommOut", ret[0], ret[1]))


@plc_api.route('/comm_in', methods=['GET', 'POST'])
def comm_in():
    """通信口插入命令"""
    logger.info("API request: Comm in")
    ret = plc_controller.comm_in()
    
    return jsonify(create_response("CommIn", ret[0], ret[1]))


@plc_api.route('/reset_out', methods=['GET', 'POST'])
def reset_out():
    """重置按钮释放命令"""
    logger.info("API request: Reset out")
    ret = plc_controller.reset_off()
    
    return jsonify(create_response("ResetOut", ret[0], ret[1]))


@plc_api.route('/reset_in', methods=['GET', 'POST'])
def reset_in():
    """重置按钮按下命令"""
    logger.info("API request: Reset in")
    ret = plc_controller.reset_on()
    
    return jsonify(create_response("ResetIn", ret[0], ret[1]))


@plc_api.route('/lane_select_out', methods=['GET', 'POST'])
def lane_out():
    """通道选择释放命令"""
    logger.info("API request: Lane select out")
    ret = plc_controller.lane_select_off()
    
    return jsonify(create_response("LANE_SELECT_Out", ret[0], ret[1]))


@plc_api.route('/lane_select_in', methods=['GET', 'POST'])
def lane_in():
    """通道选择按下命令"""
    logger.info("API request: Lane select in")
    ret = plc_controller.lane_select_on()
    
    return jsonify(create_response("LANE_SELECT_In", ret[0], ret[1]))


@plc_api.route('/cradle_insert', methods=['GET', 'POST'])
def cradle_insert():
    """托架插入命令"""
    logger.info("API request: Cradle insert")
    ret = plc_controller.cradle_inserted()
    
    return jsonify(create_response("CRADLE_INSERT", ret[0], ret[1]))


@plc_api.route('/cradle_extract', methods=['GET', 'POST'])
def cradle_extract():
    """托架拔出命令"""
    logger.info("API request: Cradle extract")
    ret = plc_controller.cradle_extracted()
    
    return jsonify(create_response("CRADLE_EXTRACT", ret[0], ret[1]))


# @plc_api.route('/PLC/Status/GetCradleState', methods=['GET', 'POST'])
# def get_cradle_state():
#     """获取托架状态"""
#     logger.info("API request: Get cradle state")
#     ret = plc_controller.get_cradle_state()
    
#     if ret[0]:
#         state = "插入" if ret[1] == 1 else "拔出"
#         return jsonify(create_response("GetCradleState", ret[0], f"Cradle state: {state} ({ret[1]})"))
#     else:
#         return jsonify(create_response("GetCradleState", ret[0], "Get cradle state failed"))


# @plc_api.route('/PLC/Status/GetFirmware', methods=['GET', 'POST'])
# def get_firmware():
#     """获取固件版本"""
#     logger.info("API request: Get firmware")
#     ret = plc_controller.get_plc_firmware()
    
#     if ret[0]:
#         return jsonify(create_response("GetFirmware", ret[0], f"Firmware version: {ret[1]}"))
#     else:
#         return jsonify(create_response("GetFirmware", ret[0], "Get firmware failed"))


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
        file_path = os.path.join(static_dir, filename)
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
        file_path = os.path.join(static_dir, filename)
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

