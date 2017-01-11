#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib


def md5file(filename):
    with open(filename, 'rb') as f:
        fcont = f.read()
        fmd5 = hashlib.md5(fcont).hexdigest()
    return fmd5

def md5str(arg):
    return hashlib.md5(bytes(arg, encoding='utf8')).hexdigest()
