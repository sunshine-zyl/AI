#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data_precess.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/6 16:48   zyli      1.0         None
'''

# import lib
import time
import requests
import pandas as pd
from app.common.errorcode import *
# default path
data_path = 'data/'
# 三步骤
# 读取数据
# 解析数据
# 保存数据为csv


# auto generate filename
# 自动生成文件名
def fn_auto_generate(kpi_name, time_type, file_type):
    """
    :param kpi_name: kpi name example(cpu_cluster_host)
    :param time_type: %Y%m%d, %Y%m%d%H%M, %Y%m%d-%H%M ,et al
    :param file_type: csv,txt,pkl,et al
    :return:
    """
    # get local time
    time_now = time.strftime(time_type, time.localtime())
    file_name = kpi_name + "_" + time_now + "." + file_type
    return file_name


def request_data(url):
    req = requests.get(url, timeout=30)  # 请求连接
    req_json = req.json()  # 获取数据
    return req_json


def parse_data(data):
    # 假设请求数据成功
    # return 一部分数据
    # 主机名和集群名：cluster_host(str)直接在接口处输入
    # 指标数据：时间戳和指标值(List->DataFrame)
    dt = data['data']
    if dt['result']:
        dr = dt['result'][0]
        data_values = dr['values']
        return data_values
    else:
        return ReqDat_ERR


def save_data(data, file_name, freq):
    df = pd.DataFrame(data, columns=['timestamp', 'index_name'])
    for i in range(len(df)):
        df.loc[i, 'time_freq'] = i % int(freq)
    file_path = data_path + file_name
    df.to_csv(file_path, index=False)
