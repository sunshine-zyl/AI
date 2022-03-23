#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   do_train.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/1 14:57   zyli      1.0         None
'''

# import lib
import numpy as np
import pandas as pd
from app.service.algorithm import xgboosting, yoystd


# # 每天的数据条数
# FREQ = 96

class TrainOperation(object):
    def __init__(self):
        self.xgb_obj = xgboosting
        self.threshold_obj = yoystd

    def start_train(self, source_data, model_save, threshold_save, freq):
        results = "success"
        contents = []
        err = self.threshold_obj.do_yoystd(filepath_in=source_data, filepath_out=threshold_save, freq=freq)
        if err:
            return err
        else:
            self.xgb_obj.xgb_train(source_data, model_save)
