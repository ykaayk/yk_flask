# coding:utf-8
from flask import Flask
import config
from exts import db, mail
from views.frontviews import postviews, accountviews
from views.cmsviews import cmsviews
from flask_wtf import CSRFProtect
import flask
from constants import FRONT_SESSION_ID, CMS_SESSION_ID
from models.frontmodels import FrontUser
from models.cmsmodels import CMSUser
from utils import xtjson
from datetime import datetime

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
db.init_app(app)
CSRFProtect(app)
mail.init_app(app)


# 注册蓝图，用蓝图来写所有视图函数
app.register_blueprint(cmsviews.bp)
app.register_blueprint(postviews.bp)
app.register_blueprint(accountviews.bp)

# manage/config/exts/models/forms/views/constants/utils/static/templates


# 钩子函数：请求之前执行，判断是否已经登陆
@app.before_request
def before_request():
    cms_id = flask.session.get(CMS_SESSION_ID)
    if cms_id:
        cms_user = CMSUser.query.get(cms_id)
        flask.g.cms_user = cms_user
    front_id = flask.session.get(FRONT_SESSION_ID)
    if front_id:
        front_user = FrontUser.query.get(front_id)
        flask.g.front_user = front_user


# 验证是否登录，若登录了则返回front_user给模板渲染使用
# 供模板渲染随时使用
@app.context_processor
def post_context_processor():
    front_id = flask.session.get(FRONT_SESSION_ID)
    if front_id:
        front_user = flask.g.front_user
        return {'front_user': front_user}
    else:
        return {}


# 上下文处理器
# 钩子函数：返回一个字典，供CMS模板使用
@app.context_processor
def cms_context_processor():
    cms_id = flask.session.get(CMS_SESSION_ID)
    if cms_id:
        user = flask.g.cms_user
        return {'cms_user': user}
    else:
        return {}


# 钩子函数，帖子过滤器
# 时间
@app.template_filter('handle_time')
def handle_time(time):
    if type(time) == datetime:
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            seconds = int(timestamp)
            return u'%s秒前' % seconds
        elif 60 <= timestamp < 60*60:
            minutes = int(timestamp / 60)
            return u'%s分钟前' % minutes
        elif 60*60 <= timestamp < 60*60*24:
            hours = int(timestamp / 60 / 60)
            return u'%s小时前' % hours
        elif 60*60*24 <= timestamp < 60*60*24*30:
            days = int(timestamp / 60 / 60 / 24)
            return u'%s天前' % days
        elif now.year == time.year:
            return time.strftime('%m-%d %H:%M:%S')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')
    return time


# 404错误页面的视图函数
@app.errorhandler(404)
def cms_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return flask.render_template('cms/cms_404.html'), 404


# 401错误页面的视图函数
@app.errorhandler(401)
def post_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.redirect(flask.url_for('account.login'))

if __name__ == '__main__':
    app.run()

