import datetime
import time
from collections import OrderedDict

from flask import Flask, render_template, session, request, copy_current_request_context, jsonify, send_from_directory

from Global import *
from flask import Response
import json
from flask_cors import CORS

api = Flask(__name__)
CORS(api)
api.config['JSON_SORT_KEYS'] = False

@api.route('/testapi.html')
def serve_testapi():
    return send_from_directory('static', 'testapi.html')

tasks = '''All can use POST or GET
<div>{
<div>   {
<div>       'URL':'http://{host}:5000/PLC/Control/ConnectPLC',</div>
<div>       'function': u'ConnectPLC',</div>
<div>       'description': u'Connect PLC with host and port,default host 192.168.1.11,default port 502',</div>
<div>       'params': u'[str,int],Host,Port',</div>
<div>       'return': u'Result:True or False,Message:Connect message or error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ConnectPLC?Host=192.168.1.11&Port=502</div>
<div>       response: {"Function":"ConnectPLC","Message":"Connect PLC Successful 192.168.1.11:502","Result":true,"timestamp":"2025-01-25 13:41:27_396084"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/DisconnectPLC',</div>
<div>       'function': u'DisconnectPLC',</div>
<div>       'description': u'Disconnect PLC',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Disconnect message or error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/DisconnectPLC</div>
<div>       response: {"Function":"DisconnectPLC","Message":"Close Successful","Result":true,"timestamp":"2025-01-25 13:43:47_847322"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/LifterUp',</div>
<div>       'function': u'LifterUp',</div>
<div>       'description': u'Control Lifter Up,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Lifter Up Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/LifterUp</div>
<div>       response: {"Function":"LifterUp","Message":"Set Lifter Up Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/LifterDown',</div>
<div>       'function': u'LifterDown',</div>
<div>       'description': u'Control Lifter Down,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Lifter Down Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/LifterDown</div>
<div>       response: {"Function":"LifterDown","Message":"Set Lifter Down Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/ClampX_Out',</div>
<div>       'function': u'ClampX_Out',</div>
<div>       'description': u'Control Clamp X Out,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Clamp X Out Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ClampX_Out</div>
<div>       response: {"Function":"ClampX_Out","Message":"Set Clamp X Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/ClampX_In',</div>
<div>       'function': u'ClampX_In',</div>
<div>       'description': u'Control Clamp X In,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Clamp X In Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ClampX_In</div>
<div>       response: {"Function":"ClampX_In","Message":"Set Clamp X In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/ClampY_Out',</div>
<div>       'function': u'ClampY_Out',</div>
<div>       'description': u'Control Clamp Y Out,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set ClampY_Out Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ClampY_Out</div>
<div>       response: {"Function":"ClampY_Out","Message":"Set Clamp Y Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/ClampY_In',</div>
<div>       'function': u'ClampY_In',</div>
<div>       'description': u'Control Clamp Y In,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Clamp Y In Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ClampY_In</div>
<div>       response: {"Function":"ClampY_In","Message":"Set Clamp Y In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/PowerOut',</div>
<div>       'function': u'PowerOut',</div>
<div>       'description': u'Control Power Out,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Power Out Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/PowerOut</div>
<div>       response: {"Function":"PowerOut","Message":"Set Power Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/PowerIn',</div>
<div>       'function': u'PowerIn',</div>
<div>       'description': u'Control Power In,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Power In Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/PowerIn</div>
<div>       response: {"Function":"PowerIn","Message":"Set Power In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/CommOut',</div>
<div>       'function': u'CommOut',</div>
<div>       'description': u'Control Comm Out,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Comm Out Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/CommOut</div>
<div>       response: {"Function":"CommOut","Message":"Set Comm Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/CommIn',</div>
<div>       'function': u'CommIn',</div>
<div>       'description': u'Control Comm In,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Comm In Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/CommIn</div>
<div>       response: {"Function":"CommIn","Message":"Set Comm In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/ResetOut',</div>
<div>       'function': u'ResetOut',</div>
<div>       'description': u'Control Reset Out,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Reset Out Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ResetOut</div>
<div>       response: {"Function":"ResetOut","Message":"Set Reset Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/ResetIn',</div>
<div>       'function': u'ResetIn',</div>
<div>       'description': u'Control Reset In Work,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set Reset In Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/ResetIn</div>
<div>       response: {"Function":"ResetIn","Message":"Set Reset In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/LANE_SELECT_Out',</div>
<div>       'function': u'LANE_SELECT_Out',</div>
<div>       'description': u'Control LANE_SELECT_Out,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set LANE_SELECT_Out Successful or Error message'</div>
<div>       'example': http://127.0.0.1:49900/PLC/Control/LANE_SELECT_Out</div>
<div>       response: {"Function":"LANE_SELECT_Out","Message":"Set LANE_SELECT_Out Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/LANE_SELECT_In',</div>
<div>       'function': u'LANE_SELECT_In',</div>
<div>       'description': u'Control LANE_SELECT_In,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set LANE_SELECT_In Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/LANE_SELECT_In</div>
<div>       response: {"Function":"LANE_SELECT_In","Message":"Set LANE_SELECT_In Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/CRADLE_INSERT',</div>
<div>       'function': u'CRADLE_INSERT',</div>
<div>       'description': u'Control CRADLE_INSERT,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set CRADLE_INSERT Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/CRADLE_INSERT</div>
<div>       response: {"Function":"CRADLE_INSERT","Message":"Set CRADLE_INSERT Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>   {</div>
<div>       'URL': 'http://{host}:5000/PLC/Control/CRADLE_EXTRACT',</div>
<div>       'function': u'CRADLE_EXTRACT',</div>
<div>       'description': u'Control CRADLE EXTRACT,if normal then Result is True,Message return Control Successful',</div>
<div>       'params': u'',</div>
<div>       'return': u'Result:True or False,Message:Set CRADLE EXTRACT Successful or Error message'</div>
<div>       'example': http://127.0.0.1:5000/PLC/Control/CRADLE_EXTRACT</div>
<div>       response: {"Function":"CRADLE_EXTRACT","Message":"Set CRADLE EXTRACT Successful","Result":true,"timestamp":"2025-01-25 13:44:32_943210"}</div>
<div>   },</div>
<div>}</div>'''


@api.route('/', methods=['GET', 'POST'])
def getTasks():
    # return jsonify({'Function': tasks})
    return tasks

@api.route('/PLC/Control/ConnectPLC', methods=['GET', 'POST'])
def connectPLC():
    host = request.args.get('Host', type=str, default='192.168.1.11')
    port = request.args.get('Port', type=int, default=502)
    ret = PLC.connectPLC(host, port)
    return jsonify({'Function':"ConnectPLC",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})


@api.route('/PLC/Control/DisconnectPLC', methods=['GET', 'POST'])
def disconnectPLC():
    ret = PLC.disconnectPLC()
    return jsonify({'Function':"DisconnectPLC",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/LifterUp', methods=['GET', 'POST'])
def lifterUp():
    ret = PLC.lifterUp()
    return jsonify({'Function':"LifterUp",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/LifterDown', methods=['GET', 'POST'])
def lifterDown():
    ret = PLC.lifterDown()
    return jsonify({'Function':"LifterDown",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/ClampX_Out', methods=['GET', 'POST'])
def clampX_out():
    ret = PLC.clampX_out()
    return jsonify({'Function':"ClampX_Out",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/ClampX_In', methods=['GET', 'POST'])
def clampX_in():
    ret = PLC.clampX_in()
    return jsonify({'Function':"ClampX_In",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/ClampY_Out', methods=['GET', 'POST'])
def clampY_out():
    ret = PLC.clampY_out()
    return jsonify({'Function':"ClampY_Out",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/ClampY_In', methods=['GET', 'POST'])
def clampY_in():
    ret = PLC.clampY_in()
    return jsonify({'Function':"ClampY_In",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/PowerOut', methods=['GET', 'POST'])
def powerOut():
    ret = PLC.powerOut()
    return jsonify({'Function':"PowerOut",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/PowerIn', methods=['GET', 'POST'])
def powerIn():
    ret = PLC.powerIn()
    return jsonify({'Function':"PowerIn",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/CommOut', methods=['GET', 'POST'])
def commOut():
    ret = PLC.commOut()
    return jsonify({'Function':"CommOut",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/CommIn', methods=['GET', 'POST'])
def commIn():
    ret = PLC.commIn()
    return jsonify({'Function':"CommIn",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/ResetOut', methods=['GET', 'POST'])
def resetOut():
    ret = PLC.reset_off()
    return jsonify({'Function':"ResetOut",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/ResetIn', methods=['GET', 'POST'])
def resetIn():
    ret = PLC.reset_on()
    return jsonify({'Function':"ResetIn",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/LANE_SELECT_Out', methods=['GET', 'POST'])
def lanOut():
    ret = PLC.lane_select_off()
    return jsonify({'Function':"LANE_SELECT_Out",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/LANE_SELECT_In', methods=['GET', 'POST'])
def lanIn():
    ret = PLC.lane_select_on()
    return jsonify({'Function':"LANE_SELECT_In",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/CRADLE_INSERT', methods=['GET', 'POST'])
def start():
    ret = PLC.cradle_inserted()
    return jsonify({'Function':"CRADLE_INSERT",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})

@api.route('/PLC/Control/CRADLE_EXTRACT', methods=['GET', 'POST'])
def stop():
    ret = PLC.cradle_extracted()
    return jsonify({'Function':"CRADLE_EXTRACT",'Result': ret[0], 'Message': ret[1],
                    'timestamp': datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S_%f")})


@api.route('/set_control', methods=['GET', 'POST'])
def set_control():
    # 检查 Content-Type
    if not request.is_json:
        response_data = {
            "state": "",
            "result": 1,
            "status": "Content-Type must be application/json"
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        ), 400


    # Get JSON data from request
    data = request.get_json()

    # Validate required fields
    if not data or 'control_name' not in data or 'control_state' not in data:
        response_data = {
            "state": "",
            "result": -1,  # Error code
            "status": "Missing required fields (control_name, control_state)"
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        ),400

    control_name = data['control_name']
    control_state = data['control_state']
    kwargs = data.get('kwargs', {})  # Optional kwargs

    ret = (1, "The control_name or control_state does not exist.")

    if control_name == "cradle":
        if control_state == "inserted":
            ret = PLC.cradle_inserted()
            ret = (0 if ret[0] else 1, ret[1])
        elif control_state == "extracted":
            ret = PLC.cradle_extracted()
            ret = (0 if ret[0] else 1, ret[1])
    elif control_name == "reset":
        if control_state == "on":
            ret = PLC.reset_on()
            ret = (0 if ret[0] else 1, ret[1])
        elif control_state == "off":
            ret = PLC.reset_off()
            ret = (0 if ret[0] else 1, ret[1])
    elif control_name == "lane_select":
        if control_state == "on":
            ret = PLC.lane_select_on()
            ret = (0 if ret[0] else 1, ret[1])
        elif control_state == "off":
            ret = PLC.lane_select_off()
            ret = (0 if ret[0] else 1, ret[1])

    response_data = {
        "state": control_state if ret[0]==0 else "",
        "result": ret[0],
        "status": "" if ret[0]==0 else ret[1]
    }

    # Return response
    return Response(
        json.dumps(response_data, ensure_ascii=False, indent=None),
        mimetype='application/json'
    )


@api.route('/get_control', methods=['GET', 'POST'])
def get_control():
    # 检查 Content-Type
    if not request.is_json:
        response_data = {
            "state": "",
            "result": 1,
            "status": "Content-Type must be application/json"
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        ), 400

    # Get JSON data from request
    data = request.get_json()

    # Validate required fields
    if not data or 'control_name' not in data:
        response_data = {
            "state": "",
            "result": 1,  # Error code
            "status": "Missing required fields (control_name, control_state)"
        }
        return Response(
            json.dumps(response_data, ensure_ascii=False, indent=None),
            mimetype='application/json'
        ), 400

    control_name = data['control_name']
    kwargs = data.get('kwargs', {})  # Optional kwargs

    ret = ("none", 1, "The control_name or control_state does not exist.")

    if control_name == "cradle":
        ret = PLC.get_cradle_state()
    elif control_name == "destaco":
        ret = PLC.get_destaco_state()
    elif control_name == "reset":
        ret = PLC.get_reset_state()
    elif control_name == "lane_select":
        ret = PLC.get_lane_select_state()

    response_data = {
        "state": ret[0],
        "result": ret[1],
        "status": ret[2]
    }

    # Return response
    return Response(
        json.dumps(response_data, ensure_ascii=False, indent=None),
        mimetype='application/json'
    )

@api.route('/get_version', methods=['GET', 'POST'])
def get_version():
    plc_firmware = PLC.get_plc_firmware()

    response_data = {
        "service_version": "1.0.0",
        "hw_rev": "5Zc3",
        "plc_firmware": plc_firmware,
    }

    # Return response
    return Response(
        json.dumps(response_data, ensure_ascii=False, indent=None),
        mimetype='application/json'
    )