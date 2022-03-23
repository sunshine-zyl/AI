#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/11 16:12   zyli      1.0         None
"""

# import lib
from flask_restplus import Swagger
from flask_restplus import fields
from flask_restplus.model import ModelBase
from flask_restplus.swagger import ref, PY_TYPES
from six import string_types
from inspect import isclass
from flask_restplus import Api
from app.apis.aiopsdetection import api as ns1
from app.apis.aiopstrain import api as ns2
from app.apis.aiopsdatamanagement import api as ns3

api = Api(
    title='smeAIOps',
    version='0.1.0',
    description='smeAIOps API',
    doc='/'
)

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)


def serialize_schema(self, model):
    if isinstance(model, string_types) and model == 'object':
        return {
            'type': 'object'
        }
    if isinstance(model, (list, tuple)):
        model = model[0]
        return {
            'type': 'array',
            'items': self.serialize_schema(model),
        }

    elif isinstance(model, ModelBase):
        self.register_model(model)
        return ref(model)

    elif isinstance(model, string_types):
        self.register_model(model)
        return ref(model)

    elif isclass(model) and issubclass(model, fields.Raw):
        return self.serialize_schema(model())

    elif isinstance(model, fields.Raw):
        return model.__schema__

    elif isinstance(model, (type, type(None))) and model in PY_TYPES:
        return {'type': PY_TYPES[model]}

    raise ValueError('Model {0} not registered'.format(model))


Swagger.serialize_schema = serialize_schema



