import re

log_path = '../Log/cURL_Centaur-9.txt'

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
last_curl = None
for i, line in enumerate(lines):
    line = line.strip()
    # 匹配带路径的curl命令
    m = re.match(r'.*>\s*(curl .+)', line)
    if m:
        last_curl = m.group(1)
        # 查找后续第一个json返回
        for j in range(i+1, len(lines)):
            resp = lines[j].strip()
            if resp.startswith('{') and resp.endswith('}'):  # 简单判断为json返回
                output.append(f'{last_curl}\n{resp}\n')
                last_curl = None
                break

print('\n'.join(output))
