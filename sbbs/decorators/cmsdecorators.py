# coding:utf8
import flask
import constants
from functools import wraps
from utils import xtjson
from models.cmsmodels import CMSPermission


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        id = flask.session.get(constants.CMS_SESSION_ID)
        if id:
            return func(*args, **kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))

    return wrapper


# 权限限制
def permission_required(permission):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if flask.g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                # 如果通过ajax的方式
                if flask.request.is_xhr:
                    return xtjson.json_unauth_error()  # 未授权
                else:
                    flask.abort(401)
        return wrapper
    return deco


# 超级管理员
def superadmin_required(func):
    return permission_required(CMSPermission.ADMINISTRATOR)(func)
