#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/10 18:30   zyli      1.0         None
'''

# import lib

from flask import Flask
from app.apis import api
app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
    # 定时器1
    # 定时进行模型的训练

    # 监控器2
    # 监控数据有变化
