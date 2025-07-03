# import os
# import sys

# # 切换到src目录，确保相对导入无误
# dir_path = os.path.dirname(os.path.abspath(__file__))
# os.chdir(os.path.join(dir_path, '../src'))
# sys.path.insert(0, os.getcwd())

from RSETAPI import api

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5001, debug=True) 