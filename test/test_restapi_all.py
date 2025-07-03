import requests
import json
from pprint import pprint

BASE_URL = 'http://127.0.0.1:5001'

# 定义所有API测试用例
TEST_CASES = [
    {
        'name': 'ConnectPLC',
        'url': '/PLC/Control/ConnectPLC',
        'method': 'GET',
        'params': {'Host': '192.168.1.11', 'Port': 502},
    },
    {
        'name': 'DisconnectPLC',
        'url': '/PLC/Control/DisconnectPLC',
        'method': 'GET',
        'params': {},
    },
    {'name': 'LifterUp', 'url': '/PLC/Control/LifterUp', 'method': 'GET', 'params': {}},
    {'name': 'LifterDown', 'url': '/PLC/Control/LifterDown', 'method': 'GET', 'params': {}},
    {'name': 'ClampX_Out', 'url': '/PLC/Control/ClampX_Out', 'method': 'GET', 'params': {}},
    {'name': 'ClampX_In', 'url': '/PLC/Control/ClampX_In', 'method': 'GET', 'params': {}},
    {'name': 'ClampY_Out', 'url': '/PLC/Control/ClampY_Out', 'method': 'GET', 'params': {}},
    {'name': 'ClampY_In', 'url': '/PLC/Control/ClampY_In', 'method': 'GET', 'params': {}},
    {'name': 'PowerOut', 'url': '/PLC/Control/PowerOut', 'method': 'GET', 'params': {}},
    {'name': 'PowerIn', 'url': '/PLC/Control/PowerIn', 'method': 'GET', 'params': {}},
    {'name': 'CommOut', 'url': '/PLC/Control/CommOut', 'method': 'GET', 'params': {}},
    {'name': 'CommIn', 'url': '/PLC/Control/CommIn', 'method': 'GET', 'params': {}},
    {'name': 'ResetOut', 'url': '/PLC/Control/ResetOut', 'method': 'GET', 'params': {}},
    {'name': 'ResetIn', 'url': '/PLC/Control/ResetIn', 'method': 'GET', 'params': {}},
    {'name': 'LANE_SELECT_Out', 'url': '/PLC/Control/LANE_SELECT_Out', 'method': 'GET', 'params': {}},
    {'name': 'LANE_SELECT_In', 'url': '/PLC/Control/LANE_SELECT_In', 'method': 'GET', 'params': {}},
    {'name': 'CRADLE_INSERT', 'url': '/PLC/Control/CRADLE_INSERT', 'method': 'GET', 'params': {}},
    {'name': 'CRADLE_EXTRACT', 'url': '/PLC/Control/CRADLE_EXTRACT', 'method': 'GET', 'params': {}},
    {
        'name': 'set_control',
        'url': '/set_control',
        'method': 'POST',
        'json': {'control_name': 'cradle', 'control_state': 'inserted', 'kwargs': {}},
    },
    {
        'name': 'get_control',
        'url': '/get_control',
        'method': 'POST',
        'json': {'control_name': 'cradle', 'kwargs': {}},
    },
    {
        'name': 'get_version',
        'url': '/get_version',
        'method': 'GET',
        'params': {},
    },
    {
        'name': 'API说明',
        'url': '/',
        'method': 'GET',
        'params': {},
    },
]

def print_result(name, resp):
    print(f'\n==== {name} ===')
    print(f'Status: {resp.status_code}')
    try:
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        if (isinstance(data, dict) and (data.get('Result') is False or data.get('result', 0) != 0)) or resp.status_code != 200:
            print('\033[91m[FAILED]\033[0m')
    except Exception:
        print(resp.text)
        if resp.status_code != 200:
            print('\033[91m[FAILED]\033[0m')

def main():
    for case in TEST_CASES:
        url = BASE_URL + case['url']
        print(f'\n请求: {case["name"]} ({case["method"]}) {url}')
        if case['method'] == 'GET':
            resp = requests.get(url, params=case.get('params', {}))
        elif case['method'] == 'POST':
            if 'json' in case:
                resp = requests.post(url, json=case['json'])
            else:
                resp = requests.post(url, data=case.get('params', {}))
        else:
            print('不支持的请求方法')
            continue
        print_result(case['name'], resp)

if __name__ == '__main__':
    main() 