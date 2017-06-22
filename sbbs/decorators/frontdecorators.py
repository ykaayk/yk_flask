# coding:utf8
from functools import wraps
import flask
import constants


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        front_user_id = flask.session.get(constants.FRONT_SESSION_ID)
        if front_user_id:
            return func(*args, **kwargs)
        else:
            return flask.redirect(flask.url_for('account.login'))
            # flask.abort(401)

    return wrapper

