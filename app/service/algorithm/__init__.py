#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/1 15:35   zyli      1.0         None
'''

# import lib
import time
import pandas as pd
from app.common.errorcode import *


# 判断网管指标是主机级指标还是网元级指标
def detect_nmi(name):
    name_str = name.split("_")
    return len(name_str)


# 从目录中解析出文件名，返回kpi_name list
def path_parse_fn(str):
    fp = str.split("/")
    fn = fp[-1:]
    td = detect_nmi(fn[0])
    if td == 3 or td == 4:
        kpi_n = fn[0].split("_")
        return kpi_n[:-1]
    else:
        return FileName_ERR


# 读取数据，返回数据和文件名
def read_data(filepath):
    fn = path_parse_fn(filepath)
    data = pd.read_csv(filepath)
    X = data['time_freq']
    y = data['index_name']
    s1 = "_"
    return X, y, s1.join(fn)


# 自动生成文件名
def fn_auto_generate(kpi_name, time_type, file_type):
    """
    :param kpi_name: kpi name example(cpu_SCPAS10_SJSCP10AS_1)
    :param time_type: %Y%m%d, %Y%m%d%H%M, %Y%m%d-%H%M ,et al
    :param file_type: csv,txt,pkl,et al
    :return:
    """
    # get local time
    time_now = time.strftime(time_type, time.localtime())
    file_name = kpi_name + "_" + time_now + "." + file_type
    return file_name
