import json
import re

def normalize_descriptions(file_path):
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 处理每一项的 description
    for item in data:
        if 'description' in item and item['description']:
            # 转小写，非字母数字替换为_
            item['description'] = re.sub(r'[^a-z0-9]', '_', item['description'].lower())

    # 写回 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 用法示例
if __name__ == '__main__':
    normalize_descriptions('src/static/io_setting_Centaur_9_Tester.json')
