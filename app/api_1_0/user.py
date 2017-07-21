# -*- coding: utf-8 -*-
from flask_login import login_required
from flask_restful import Resource
from ..models import User
from ..response import BaseResponse


class UserResource(Resource):
    @login_required
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        result = {}

        if user is not None:
            result['id'] = user.id
            result['username'] = user.username
            result['phone'] = user.phone
            result['email'] = user.email

        return BaseResponse(result=result).get_response()
