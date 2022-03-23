#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   aiopsdatamanagement.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/6 9:48   zyli      1.0         None
'''

# import lib
from flask import jsonify
from flask_restplus import Namespace, Resource
from app.common.errorcode import *
import app.service.datamanagement.data_precess as dp

ADDR = 'addr'
EXPR = 'expr'
START = 'startime'
END = 'endtime'
STEP = 'step'
INDEX = 'idxnm'
CLUSTER = 'clsnm'
HOST = 'hosnm'
FREQ = 'freq'
# create Namespace
api = Namespace("aiopsdatamanagement", path="/", description="数据管理")

# 创建请求解析器
parser = api.parser()
# 添加参数
parser.add_argument(ADDR, required=True, default='http://10.1.60.161:9090', help='数据源地址')
parser.add_argument(EXPR, required=True, default='(1-sum('
                                                   'increase(node_cpu_seconds_total{mode="idle", '
                                                   'pod="omc-db-1.navalocal",moDn="omc"}[1m]))by(pod,'
                                                   'moDn)/sum(increase(node_cpu_seconds_total{'
                                                   'pod="omc-db-1.navalocal",moDn="omc"}[1m]))by(pod, '
                                                   'moDn))*100', help='表达式')
#  2021-09-04 00:00:00
parser.add_argument(START, required=True, default='1630684800', help='开始时间')
# 2021-09-07 00:00:00
parser.add_argument(END, required=True, default='1630944000', help='结束时间')
parser.add_argument(STEP, required=True, default='15m', help='步长')

# omc-db-1.navalocal,omc-db-3.novalocal,omc-web.novalocal
parser.add_argument(INDEX, required=True, default='cpu', help='指标名')
parser.add_argument(CLUSTER, required=True, default='omc', help='集群名')
# 'omc-db-1.navalocal'
parser.add_argument(HOST, required=False, help='主机名')
parser.add_argument(FREQ, required=True, default='96', help='数据条数/天 OR 数据条数/小时')


# 指定路径
@api.route('/v1/sme/AI/aiops/datmgt')
class AiopsDataManagement(Resource):
    # 添加接口描述
    @api.doc(description="查询性能指标数据")
    # 指定请求参数
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # congPrometheus获取数据，查询数据
    def get(self):
        args = parser.parse_args()
        result = 'SUCCESS'
        content = []
        # 获取参数
        addr = args.get(ADDR)
        expr = args.get(EXPR)
        start_time = args.get(START)
        end_time = args.get(END)
        step = args.get(STEP)
        index_name = args.get(INDEX)
        cluster_name = args.get(CLUSTER)
        host_name = args.get(HOST)
        fq = args.get(FREQ)
        # execute
        url = addr + '/api/v1/query_range?query=' + expr + '&start=' + start_time + '&end=' + end_time + '&step=' + step
        data = dp.request_data(url)
        if data:
            dv = dp.parse_data(data)
            if dv == 108:
                result = 'error'
                content.append(ReqDat_ERR)
            else:
                if host_name:
                    kpin = index_name + '_' + cluster_name + '_' + host_name
                else:
                    kpin = index_name + '_' + cluster_name

                fn = dp.fn_auto_generate(kpi_name=kpin, time_type="%Y%m%d", file_type='csv')
                dp.save_data(data=dv, file_name=fn, freq=fq)
        else:
            result = 'error'
            content.append(ReqDat_ERR)
        d = {
            'result': result,
            'content': content
        }
        return jsonify(d)

