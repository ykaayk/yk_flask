# coding:utf8

from flask import Blueprint, views
import flask
from exts import db
import top.api
import constants
from utils import xtjson, xtcache
from utils.captcha.xtcaptcha import Captcha
from forms.frontforms import FrontRegistForm, FrontLoginForm, SettingsForm
from models.frontmodels import FrontUser
from datetime import datetime
from decorators.frontdecorators import login_required
try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

bp = Blueprint('account', __name__, url_prefix='/account')


# 首页
@bp.route('/')
def index():
    return 'front user page'


# 注册前台用户
class RegistView(views.MethodView):

    def get(self, message=None, **kwargs):
        context = {
            'message': message,
        }
        context.update(kwargs)
        return flask.render_template('front/front_regist.html', **context)

    def post(self):
        form = FrontRegistForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            if FrontUser.query.filter(FrontUser.telephone == telephone).first():
                return self.get(message=u'此手机号码已经被注册过！', username=username)
            if FrontUser.query.filter(FrontUser.username == username).first():
                return self.get(message=u'此用户名已经被注册过！', telephone=telephone)

            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            # return flask.render_template('front/front_base.html')
            return flask.redirect(flask.url_for('post.index'))
        else:
            telephone = flask.request.form.get('telephone')
            username = flask.request.form.get('username')
            sms_captcha_repeat = flask.request.form.get('sms_captcha')
            return self.get(message=form.get_error(), telephone=telephone, sms_captcha_repeat=sms_captcha_repeat, username=username)

bp.add_url_rule('/regist/', view_func=RegistView.as_view('regist'))


# 前台用户登录
class LoginView(views.MethodView):

    def get(self, message=None, **kwargs):
        context = {
            'message': message,
        }
        context.update(kwargs)
        return flask.render_template('front/front_login.html/', **context)

    def post(self):
        form = FrontLoginForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = FrontUser.query.filter_by(telephone=telephone).first()

            if user and user.check_password(password):
                # 是否拉黑
                if not user.is_active:
                    return self.get(message=u'该用户已被拉黑！请联系管理员！')
                # 最近登录时间
                if user.old_login_time:
                    user.last_login_time = user.old_login_time
                now = datetime.now()
                user.old_login_time = now
                last = user.last_login_time
                # 登陆时间相差一天以上，积分+2
                if not last or last.year < now.year or last.month < now.month or last.day < now.day:
                    user.points += 2
                db.session.commit()
                # 做登录操作
                flask.session[constants.FRONT_SESSION_ID] = user.id
                # 是否记住用户
                if remember:
                    flask.session.permanent = True
                return flask.redirect(flask.url_for('post.index'))
                # return flask.render_template('front/front_index.html')
            else:
                return self.get(message=u'用户名不存在或者密码错误')
        else:
            return self.get(message=form.get_error())

bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


# 注销登录
@bp.route('/logout/')
def logout():
    try:
        flask.session.pop(constants.FRONT_SESSION_ID)
        # retur flask.redirect(flask.url_for('account.login'))
        return flask.render_template('front/front_logout.html')
    except:
        return flask.redirect(flask.url_for('post.index'))


# 个人设置
@bp.route('/settings/', methods=['GET', 'POST'])
@login_required
def setting():
    if flask.request.method == 'GET':
        return flask.render_template('front/front_setting.html')
    else:
        form = SettingsForm(flask.request.form)
        if form.validate():
            realname = form.realname.data
            qq = form.qq.data
            head_img = form.head_img.data
            gender = form.gender.data
            signature = form.signature.data
            front_model = flask.g.front_user
            if realname:
                front_model.realname = realname
            if qq:
                front_model.qq = qq
            if head_img:
                front_model.head_img = head_img
            if gender:
                front_model.gender = gender
            if signature:
                front_model.signature = signature
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 个人信息中心
@bp.route('/personal_center/')
@login_required
def personal_center():
    contest = {
        'user': flask.g.front_user
    }
    return flask.render_template('front/front_personal_center.html', **contest)


# 短信验证码
@bp.route('/sms_captcha/')
def sms_captcha():
    telephone = flask.request.args.get('telephone')
    if not telephone:
        return xtjson.json_params_error(message=u'必须指定手机号码！')

    if xtcache.get(telephone):
        return xtjson.json_params_error(message=u'验证码已经发送，请等待1分钟后再次发送！')

    if len(telephone) != 11:
        return xtjson.json_params_error(message=u'手机号码格式不正确，请重新填写！')

    try:
        int(telephone)
    except Exception, e:
        print e
        return xtjson.json_params_error(message=u'手机号码格式不正确，请重新填写！')

    captcha = Captcha.gene_text()
    app_key = constants.ALIDAYU_APP_KEY
    app_secret = constants.ALIDAYU_APP_SECRET
    req = top.setDefaultAppInfo(app_key, app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend = ""
    req.sms_type = 'normal'
    req.sms_free_sign_name = constants.ALIDAYU_APP_SIGN_NAME
    req.sms_param = constants.ALIDAYU_APP_PARAM % ('Jay', captcha)
    req.rec_num = telephone.decode('utf-8').encode('ascii')
    req.sms_template_code = constants.ALIDAYU_APP_TEMPLATE_CODE
    try:
        print '短信验证码是：', captcha
        # 设置缓存
        xtcache.set(telephone, captcha)
        resp = req.getResponse()
        return xtjson.json_result()
    except Exception, e:
        print e
        if e.submsg == u'触发业务流控':
            return xtjson.json_method_error(message=u'发送验证码过于频繁，请于一小时后再注册！')

        return xtjson.json_method_error(message=u'系统繁忙')


# 图片验证码
@bp.route('/graph_captcha/')
def graph_captcha():
    # 验证码过期时间，默认2分钟
    timeout = flask.request.args.get('timeout', 2, int)
    print 'timeout:', timeout
    text, image = Captcha.gene_code()
    out = StringIO()  # StringIO相当于是一个管道
    image.save(out, 'png')  # 把image塞到StingIO这个管道中
    out.seek(0)  # 将StringIO的指针指向开始的位置

    # 生成一个响应对象，out.read是把图片流给读出来
    response = flask.make_response(out.read())
    # 指定响应的类型
    response.content_type = 'image/png'
    xtcache.set(text.lower(), text.lower(), timeout=timeout*60)
    return response

# 图片验证码
# @bp.route('/test_captcha/')
# def test_captcha():
#     from utils.captcha.xtcaptcha import Captcha
#     try:
#         from StringIO import StringIO
#     except:
#         from io import BytesIO as StringIO
#
#     text, image = Captcha.gene_code()
#     # StringIO相当于一个管道
#     out = StringIO()
#     # 把image塞到StringIO这个管道里
#     image.save(out, 'png')
#     # 将StringIO的指针指向开始的位置
#     out.seek(0)
#
#     # 生成一个响应对象，out.read是把图片流给读出来
#     response = flask.make_response(out.read())
#     response.content_type = 'image/png'
#     return response




















