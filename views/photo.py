#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imghdr  # 读取文件开头少量数据来判断是否是图片，比较准确
import settings
import hashlib

root = settings.root()


def md5file(filename):
    with open(filename, 'rb') as f:
        fcont = f.read()
        fmd5 = hashlib.md5(fcont).hexdigest()
    return fmd5


def md5str(arg):
    return hashlib.md5(bytes(arg, encoding='utf8')).hexdigest()


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


def photoinfo(imgurl):
    imgpath = imgurl.replace('/static/mountfile/', '', 1)
    imgfile = os.path.normpath(os.path.join(root, imgpath))
    imgmd5 = md5file(imgfile)
    try:
        imgname = imgpath.rsplit('/', 1)[1]
        imgdir = imgpath.rsplit('/', 1)[0]
    except IndexError as e:
        imgname = imgpath
        imgdir = '/'
    imgdirmd5 = md5str(imgdir)

    retdict = {
        "imgmd5": imgmd5,
        "imgname": imgname,
        "imgdirmd5": imgdirmd5,
        "imgdir": imgdir
    }
    return retdict
