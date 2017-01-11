#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# 根目录配置
# 要求将浏览的文件目录挂载到statics/mountfile目录，没有对任意位置的目录做兼容性测试，因为我准备使用docker容器运行程序，正好是挂载方式。
# 使用normpath对windows和linux的路径分隔符做兼容
baseroot = os.path.normpath(os.path.join(os.path.dirname(__file__), 'statics/mountfile'))

def root():
    return baseroot

# 数据库配置
dbconfig={
    'DBHost': '10.0.0.24',
    'DBPort': '3306',
    'User': 'root',
    'Pwd': '123456',
    'Database': 'zyimg'
}


def mysqlconfig():
    return dbconfig
