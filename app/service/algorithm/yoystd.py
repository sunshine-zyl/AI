#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   yoystd.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/31 10:23   zyli      1.0         None
'''

# import lib
import pandas as pd
import numpy as np
from app.service.algorithm import *
import os
from app.common.errorcode import *


# 同比计算
def yoy_compute(data, cicle_num, sign=False):
    """

    :param cicle_num:
    :param sign:
    :param data: np.ndarray
    :return: yoy_std:shape(n, 1)
    """
    n = int(len(data) / cicle_num)
    # 重置矩阵shape：n行7列，按列读取
    df_v_new = data.reshape((n, cicle_num), order='F')
    # print(df_v_new[245:255, :])
    if not sign:
        yoy_std = np.std(df_v_new, axis=1)
        return yoy_std
    else:
        d_mean = np.mean(df_v_new, axis=1)
        return d_mean


# 环比计算
def rr_compute(data, cicle_num):
    """

    :param data:
    :param cicle_num:
    :return: rr_std:shape(n,1)
    """
    # 每天的第一个值环比,6points
    first_diff = []
    # 除以上值环比的其余值
    other_diff = []
    # 每天值的数量
    n = int(len(data) / cicle_num)
    for i in range(len(data) - 1):
        if ((i + 1) % n) == 0:
            diff = abs(data[i + 1] - data[i])
            first_diff.append(diff)
        else:
            diff = abs(data[i + 1] - data[i])
            other_diff.append(diff)
    fd = np.mean(first_diff)
    sign = True
    rr_std = yoy_compute(np.array(other_diff), cicle_num, sign=sign)
    rr_std = np.insert(rr_std, 0, [fd], axis=0)
    return rr_std


# 检测阈值计算
def detection_threshold_compute(arr_1, arr_2):
    """

    :param arr_1: yoy_std
    :param arr_2: rr_std
    :return:
    """
    # yoy - rr
    std_diff = abs(np.subtract(arr_1, arr_2))
    return std_diff


# 检测阈值算法
def do_yoystd(filepath_in, filepath_out, freq):
    x, dt, fn = read_data(filepath_in)
    if len(dt) < int(freq) * 2:
        return Freq_ERR
    else:
        freq_num = len(dt) // int(freq)
        print(freq_num)
        if len(dt) % int(freq) != 0:
            dt = dt.iloc[0: freq_num * int(freq)]
        yoy = yoy_compute(dt.values, freq_num)
        rr = rr_compute(dt.values, freq_num)
        yoystd = detection_threshold_compute(yoy, rr)
        #   保存阈值到文件中
        threshold_name = fn_auto_generate(kpi_name=fn, time_type="%Y%m%d", file_type="txt")
        if not os.path.exists(filepath_out):
            os.makedirs(filepath_out)
        output_threshold_name = os.path.join(filepath_out, threshold_name)
        np.savetxt(output_threshold_name, yoystd, fmt="%.5f", delimiter="\n")
        print("threshold save successfully!")

# if __name__ == '__main__':
#     fp = "D:/Users/EB/AppData/Local/PycharmProjects/smeAIOps_0812/data/cpu_SCPAS10_SJSCP10AS_20191001-07.csv"
#     # 读取数据
#     # data = read_file(fp)
#     # print(data)
#     # # 检验数据是否满足正态分布pv>0.05满足
#     # sts, pv = sts.kstest(data[96: 192], 'norm', (data[96: 192].mean(), data[96: 192].std()))
#     # print("pv=%.3f" % pv)
#     # yoy = yoy_compute(data, 7)
#     # rr = rr_compute(data, 7)
#     # std_diff = detection_threshold_compute(yoy, rr)
#     # # print(len(std_diff))
#     # # print(rr)
#     # plt.plot(std_diff)
#     # plt.show()
#     # l_v = []
#     # for i in range(249, len(df_v), 288):
#     #     l_v.append(df_v[i])
#     # v = np.std(l_v)
#     # print(l_v)
#     # print(v)
