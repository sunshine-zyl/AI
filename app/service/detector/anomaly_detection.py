#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   anomaly_detection.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/1 10:53   zyli      1.0         None
'''

# import lib
from datetime import datetime
import time
import pickle
import os

import numpy as np

from app.common.errorcode import *
model_path = 'model_base/'
threshold_path = 'detection_threshold/'


# 时间戳转换
def time_tran(timestamp, freq):
    """

    :param timestamp: 时间戳
    :param freq: 相邻两点的时间间隔（min）
    :return: 预测数据对应的X值
    """
    time_new = []
    # 根据时间戳转换成对应的时间序列并进行检测
    for i in range(len(timestamp)):
        t = timestamp[i]
        # 对时间戳做处理使之变成时间序列
        date_ymd = time.strftime("%Y-%m-%d %H:%M", time.localtime(t))
        w = datetime.strptime(date_ymd, "%Y-%m-%d %H:%M").weekday()
        h = datetime.strptime(date_ymd, "%Y-%m-%d %H:%M").hour
        m = datetime.strptime(date_ymd, "%Y-%m-%d %H:%M").minute
        if freq == 15:
            # 15分钟取一个点，x轴为一周的时间序列。即[0, 671] cpu
            ts_15 = h * 4 + (m // 15)
            time_new.append(ts_15)
        elif freq == 5:
            # 5分钟取一个点，x轴为一周的时间序列。即[0, 2015] caps
            ts_5 = h * 12 + (m // 5)
            time_new.append(ts_5)
        else:
            print("暂未开发！")
        # # 1分钟取一个点，x轴为一天的时间序列。即[0, 1439]
        # ts_1 = h * 60 + m
    return time_new


class AnomalyDetection(object):
    def __init__(self):
        self.model = model_path
        self.threshold = threshold_path

    # 判断模型或阈值文件是否存在
    def detect_model_or_threshold(self, parm_s):
        # names
        names = []
        sign = 0
        # errors
        errs = []
        model_names = os.listdir('model_base/')
        threshold_names = os.listdir('detection_threshold/')
        # 判断模型是否存在
        for model_name in model_names:
            if parm_s in model_name:
                print(os.path.dirname(model_name))
                names.append(model_name)
                sign += 1
                break
        # 判断阈值文件是否存在
        for threshold_name in threshold_names:
            if parm_s in threshold_name:
                print(os.path.dirname(threshold_name))
                names.append(threshold_name)
                break
        if len(names) == 0:  # 模型文件和阈值文件均不存在
            errs.append(Model_ERR)
            errs.append(Threshold_ERR)
        elif len(names) == 1 and sign == 1:  # 阈值文件不存在
            errs.append(Threshold_ERR)
        elif len(names) == 1 and sign == 0: # 模型文件不存在
            errs.append(Model_ERR)
        else:
            print("ok!")
        return names, errs

    # 异常检测
    def do_ad(self, parm_s, t, value):
        # 错误
        errs = []
        # 异常结果
        global y_pre, d_ts, time_new
        result_ano = {}
        # 异常时间戳
        time_list = []
        # 调用时间戳转换函数
        if "cpu" in parm_s:
            time_new = time_tran(timestamp=t, freq=15)
        elif "caps" in parm_s:
            time_new = time_tran(timestamp=t, freq=5)
        else:
            errs.append(TimeTran_ERR)
        nms, ers = self.detect_model_or_threshold(parm_s)
        if len(nms) == 2:  # 检测
            # 检测异常
            model = pickle.load(open(self.model + nms[0], "rb"))
            y_pre = model.predict(np.array(time_new))
            d_ts = np.loadtxt(self.threshold + nms[1])
            for i in range(len(time_new)):
                # 预测值-实际值的绝对值大于等于阈值，即为异常，返回当前时间和指标
                if abs(y_pre[i] - value[i]) >= d_ts[time_new[i]]:
                    time_list.append(t[i])
            if len(time_list) != 0:
                result_ano['indicator_name'] = parm_s
                result_ano['ano_time'] = time_list
        else:
            errs.append(ers)
        return result_ano, errs

    # # 查找对应阈值
    # def find_time_thromd(self, time):
