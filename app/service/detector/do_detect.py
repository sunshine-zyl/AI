#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   do_detect.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/2 10:22   zyli      1.0         None
'''

# import lib
from app.service.detector import anomaly_detection, process_service


class DetectOperation(object):
    def __init__(self):
        self.process_obj = process_service
        self.ad_obj = anomaly_detection.AnomalyDetection()

    def start_detect(self, data):
        # 错误集合
        err_s = []
        # 异常结果
        results = []
        detect_data, errors = self.process_obj.do_the_all_preprocess(data)
        if detect_data:
            for dt in detect_data:
                result, err = self.ad_obj.do_ad(dt["par_s"], dt["timestamp"], dt["value"])
                if err:
                    err_s.append(err)
                else:
                    if result:
                        results.append(result)
        else:
            err_s.append(errors)
        return results, err_s