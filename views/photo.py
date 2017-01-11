#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imghdr  # 读取文件开头少量数据来判断是否是图片，比较准确
import settings

root = settings.root()

def dircontent(arg):
    current_dir = os.path.normpath(os.path.join(root, arg))

    if os.path.isdir(current_dir):
        dic = {
            'dir': [],
            'img': [],
            'oth': []
        }
        for m in os.listdir(current_dir):
            fullpath = os.path.join(current_dir, m)
            if os.path.isdir(fullpath):
                dic['dir'].append(m)
            elif imghdr.what(fullpath):
                dic['img'].append(m)
            else:
                dic['oth'].append(m)

        return dic
