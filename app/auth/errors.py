# -*- coding: utf-8 -*-
from . import auth
from ..response import BaseResponse


@auth.app_errorhandler(401)
def unauthorized(error):
    return BaseResponse(code='401000', status=401).get_response()
