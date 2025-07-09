import os
import json

txt_path = 'PLC_IO.txt'
json_path = os.path.join( '..', 'src', 'static', 'PLC_IO_List_A01.json')

data = []
with open(txt_path, encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines[1:]:  # 跳过表头
        parts = line.strip().split('\t')
        if not parts or not parts[0]:
            continue
        plc = parts[0]
        desc = parts[1] if len(parts) > 1 else ""
        data.append({"PLC": plc, "description": desc})

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)