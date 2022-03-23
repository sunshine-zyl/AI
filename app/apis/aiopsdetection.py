import json
import os
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, marshal
from app.service.detector import do_detect
detect = do_detect.DetectOperation()
model_path = 'model_base/'


# 创建NameSpace
api = Namespace("aiopsdetection", path="/", description="指标异常检测")
# # define model
# model = api.model('body', {
#     'name': fields.String,
#     'age': fields.Integer
# })
# mdl_body = api.clone('mdl_body', model)
# # data = {
# #     'name': 'Bob',
# #     'age': 15
# # }

# # 创建请求解析器
# parser = api.parser()
# # 添加参数
# parser.add_argument("body", required=True, type=dict, location='form')


# 指定路径
@api.route('/v1/sme/AI/aiops/detection')
class AiopsDetection(Resource):
    # 添加接口描述
    @api.doc(description="指标异常检测并返回结果")
    # # 指定请求参数
    # @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self):
        json_data = request.get_data()
        print(json_data)
        results, errors = detect.start_detect(json_data)
        d = {
            'results': results,
            'errors': errors
        }
        return jsonify(d)

    # 添加接口描述
    @api.doc(description="查看模型库模型列表")
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    #  查看当前检测算法模型列表
    def get(self):
        models = os.listdir(model_path)
        return jsonify(models)

    # 添加接口描述
    @api.doc(description="删除模型")
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 删除当前检测算法模型列表
    def delete(self):
        return jsonify()
# /v1/sme/AI/aiops/detection  post  --> 检测   get -->  delete --  删除xxx    restful
# /v1/smeAI/aiops/train    get
