# -*- coding: utf-8 -*-
from flask import jsonify, make_response
from .codemsg import CodeMsg


class BaseResponse:
    """http请求响应"""

    def __init__(self, code='000000', result=None, status=200):
        """
        响应构造
        :param code: 响应码
        :param result: 响应体
        :param status: http状态
        """
        self.code = code
        self.msg = CodeMsg.get_msg(code)
        self.result = result
        self.status = status

    def get_response(self):
        resp_dict = {
            'code': self.code,
            'msg': self.msg,
        }
        if self.result is not None:
            resp_dict['result'] = self.result

        resp = make_response(jsonify(resp_dict), self.status)
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp
