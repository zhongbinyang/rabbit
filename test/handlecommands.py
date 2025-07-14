import json
import re

def generate_curl_commands(json_path, output_bat):
    with open(json_path, 'r', encoding='utf-8') as f:
        actions = json.load(f)

    lines = ['@echo off', '']
    for item in actions:
        action = item.get('action')
        readonly = item.get('readonly', False)
        # 拆分 action
        if '_' in action:
            idx = action.rfind('_')
            control_name = action[:idx]
            control_state = action[idx+1:]
        else:
            control_name = action
            control_state = ''
        if readonly:
            # get_control 只用 control_name
            json_data = f'{{"control_name": "{control_name}"}}'
        else:
            # set_control 用 control_name 和 control_state
            if control_state:
                json_data = f'{{"control_name": "{control_name}", "control_state": "{control_state}"}}'
            else:
                json_data = f'{{"control_name": "{control_name}"}}'
        # 外层双引号，内部所有双引号转义
        json_data_escaped = json_data.replace('"', '\\"')
        if readonly:
            cmd = (
                'curl -X POST --url http://192.168.137.175:5001/get_control '
                '-H "content-type: application/json" '
                f'-d "{json_data_escaped}"'
            )
        else:
            cmd = (
                'curl -X POST --url http://192.168.137.175:5001/set_control '
                '-H "content-type: application/json" '
                f'-d "{json_data_escaped}"'
            )
        lines.append(cmd)
        lines.append('echo.')
        lines.append('timeout /t 2 >nul')
        lines.append('')
    lines.append('pause')

    with open(output_bat, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    generate_curl_commands(
        'src/static/action_setting_Centaur_9_Tester_A02.json',
        'test/testcommand.bat'
    )