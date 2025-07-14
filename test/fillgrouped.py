import json
import os

# 路径
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../src/static/io_setting_Centaur_9_Tester.json')
grouped_path = os.path.join(base_dir, '../src/static/PLC_IO_List_A01_grouped.json')

# 读取PLC_IO_List_A01.json
with open(json_path, encoding='utf-8') as f:
    plc_list = json.load(f)

grouped = []
for item in plc_list:
    plc = item['PLC']
    desc = item['description']
    grouped.append({
        "action": desc,
        "commands": [
            {
                "command": plc
            }
        ],
        "description": plc,
        "readonly": False
    })

with open(grouped_path, 'w', encoding='utf-8') as f:
    json.dump(grouped, f, ensure_ascii=False, indent=2)
