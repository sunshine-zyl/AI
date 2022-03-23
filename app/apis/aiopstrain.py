#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   aiopstrain.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/11 16:04   zyli      1.0         None
'''

# import lib
import os
from flask import jsonify
from flask_restplus import Namespace, Resource
from app.service.train import do_train
from app.service.algorithm import *
from app.common.errorcode import *

SRCDAT = 'srcdat'
MODSP = 'mdlsave'
TRSSP = 'trslsave'
FREQ = 'freq'
# 初始化
train = do_train.TrainOperation()
data_path = 'data/'
# 创建NameSpace
api = Namespace("aiopstrain", path="/", description="模型训练")

# 创建请求解析器
parser = api.parser()

# 添加参数
parser.add_argument(SRCDAT, required=True, default='data/caps_SCPAS10_20191001-07.csv', location='form',
                    help='请输入文件名及对应目录')
parser.add_argument(MODSP, default='model_base/',
                    location='form', help='请输入目录，不包括文件名')
parser.add_argument(TRSSP, default='detection_threshold/', location='form')
parser.add_argument(FREQ, required='True', default='96', help='数据条数/天 OR 数据条数/小时')


# 指定路径
@api.route('/v1/sme/AI/aiops/train')
class AiopsTrain(Resource):
    # 添加接口描述
    @api.doc(description="训练模型及自动生成阈值")
    # 指定请求参数
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self):
        args = parser.parse_args()
        result = 'SUCCESS'
        content = []
        # 获取参数
        file_input = args.get(SRCDAT)
        model_save_out = args.get(MODSP)
        threshold_save_out = args.get(TRSSP)
        fq = args.get(FREQ)
        # content.append(file_input)
        # 文件不存在，文件名格式不正确判断，最后执行训练
        if not (os.path.exists(file_input)) or (path_parse_fn(file_input) == 104):
            result = 'error'
            content.append(FileName_ERR)
        else:
            err = train.start_train(file_input, model_save_out, threshold_save_out, freq=fq)
            if err:
                result = 'error'
                content.append(err)
        d = {
            'result': result,
            'content': content
        }
        return jsonify(d)

    # 添加接口描述
    @api.doc(description="查询源数据文件名")
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    def get(self):
        datas = os.listdir(data_path)
        return jsonify(datas)
# /v1/sme/AI/aiops/detection  post  --> 检测   get -->  delete --  删除xxx    restful
# /v1/smeAI/aiops/train    get
