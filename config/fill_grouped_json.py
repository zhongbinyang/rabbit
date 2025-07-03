import json
import random

# 文件路径
item_path = 'PLC_IO_List_A01.json'
grouped_path = 'PLC_IO_List_A01_grouped.json'
out_path = 'PLC_IO_List_grouped_filled.json'

# 读取 item 列表
with open(item_path, 'r', encoding='utf-8') as f:
    items = json.load(f)

# 读取 grouped 列表
with open(grouped_path, 'r', encoding='utf-8') as f:
    grouped = json.load(f)

# 随机填充，只保留PLC字段
for group in grouped:
    commands_len = len(group.get('commands', []))
    group['commands'] = [
        random.choice(items)['PLC'] for _ in range(commands_len)
    ]

# 保存结果
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(grouped, f, ensure_ascii=False, indent=4)

print(f'已生成: {out_path}')
