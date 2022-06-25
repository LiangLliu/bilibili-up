# 繁体转简体.py
import os
import stat

from langconv import *

root_path = './测试'


# root_path=r'K:\新建文件夹\test'

def chmod(path):
    os.chmod(path, stat.S_IWRITE)
    os.chmod(path, stat.S_IRWXO)
    os.chmod(path, stat.S_IRWXU)


def convert(root_path):
    for root, dirs, files in os.walk(root_path):
        for dir in dirs:
            chmod(os.path.join(root, dir))
            new_dir = Converter('zh-hans').convert(dir)
            if new_dir != dir:
                os.rename(os.path.join(root, dir), os.path.join(root, new_dir))
                print(os.path.join(root, dir))
        for file in files:
            chmod(os.path.join(root, file))
            new_file = Converter('zh-hans').convert(file)
            if new_file != file:
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
                print(os.path.join(root, file))

        # print(file)


if __name__ == '__main__':
    convert(root_path)
