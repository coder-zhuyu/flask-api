# -*- coding: utf-8 -*-
from flask import request, current_app
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from ..response import BaseResponse
from schema import Schema


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    passwd = request.form.get('password')

    Schema(basestring).validate(email)
    Schema(basestring).validate(passwd)

    # if not email or not passwd:
    #     current_app.logger.error(u"登录失败: emial或passwd未传")
    #     return BaseResponse(code='400001').get_response()

    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(passwd):
        login_user(user, 1)
        return BaseResponse().get_response()
    current_app.logger.error(u"登录失败: 用户不存在或者密码错误")
    return BaseResponse(code='401001').get_response()


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return BaseResponse().get_response()
