# -*- coding: utf-8 -*-
from . import auth
from ..response import BaseResponse
from ..exceptions import ValidationError


def bad_request(message):
    return BaseResponse(code='400000', result=message, status=400).get_response()


# @auth.app_errorhandler(401)
# def unauthorized(error):
#     return BaseResponse(code='401000', status=401).get_response()
#
#
# @auth.app_errorhandler(403)
# def forbidden(error):
#     return BaseResponse(code='403000', status=403).get_response()
#
#
# @auth.app_errorhandler(404)
# def page_not_found(error):
#     return BaseResponse(code='404000', status=404).get_response()
#
#
# @auth.app_errorhandler(500)
# def internal_server_error(error):
#     return BaseResponse(code='500000', status=500).get_response()


@auth.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
