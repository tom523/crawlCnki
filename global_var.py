# -*- coding: utf-8 -*-
def _init():
    global _conf_dic
    _conf_dic = {}

def set_value(name, value):
    _conf_dic[name] = value

def get_value(name, defValue=None):
    try:
        return _conf_dic[name]
    except KeyError:
        return defValue