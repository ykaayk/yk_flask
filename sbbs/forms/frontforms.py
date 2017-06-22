# coding:utf8

from baseforms import BaseForm
from wtforms import StringField, ValidationError, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, URL
from utils import xtcache


class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[InputRequired(message=u'必须输入图形验证码！')])

    # 图片验证码验证
    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        cache_captcha = xtcache.get(graph_captcha.lower())
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message=u'图形验证码错误！')
        return True


# 继承图片验证
# 前台注册用户表单验证
class FrontRegistForm(GraphCaptchaForm):
    telephone = StringField(validators=[InputRequired(message=u'必须输入手机号码！'), Length(11, 11, message=u'手机号格式不对！')])
    sms_captcha = StringField(validators=[InputRequired(message=u'必须输入短信验证码！')])
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    password = StringField(validators=[InputRequired(message=u'必须输入密码！'), Length(6, 20, message=u'密码长度必须在6-20个字符！')])
    password_repeat = StringField(validators=[EqualTo('password', message=u'两次输入密码不一致！')])
    # graph_captcha = StringField(validators=[InputRequired(message=u'必须输入图形验证码！')])

    # 短信验证码验证
    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        cache_captcha = xtcache.get(telephone)
        if not cache_captcha or cache_captcha.lower() != sms_captcha.lower():
            raise ValidationError(message=u'短信验证码错误！')
        return True


# 继承图片验证
# 前台用户登录验证表单
class FrontLoginForm(GraphCaptchaForm):
    # graph_captcha = StringField(validators=[InputRequired(message=u'必须输入图形验证码！')])
    telephone = StringField(validators=[InputRequired(message=u'必须输入手机号码！'), Length(11, 11, message=u'手机号格式不对！')])
    password = StringField(validators=[InputRequired(message=u'必须输入密码！'), Length(6, 20, message=u'密码长度必须在6-20个字符之间！')])
    remember = IntegerField()


# 新增帖子表单
class AddPostForm(GraphCaptchaForm):
    title = StringField(validators=[InputRequired(message=u'必须输入标题！')])
    content = StringField(validators=[InputRequired(message=u'必须输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message=u'必须输入板块id！')])


# 评论表单
class AddCommentForm(BaseForm):
    post_id = StringField(validators=[InputRequired(message=u'必须输入帖子id！')])
    content = StringField(validators=[InputRequired(message=u'必须输入内容！')])


# 子评论
class AddReply(BaseForm):
    comment_id = StringField(validators=[InputRequired(message=u'必须输入帖子id！')])
    reply = StringField(validators=[InputRequired(message=u'必须输入评论内容！')])


# 点赞
class StarPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须输入帖子id！')])
    is_star = BooleanField(validators=[InputRequired(message=u'必须输入赞的行为！')])


# 修改个人信息
class SettingsForm(BaseForm):
    gender = StringField()
    realname = StringField()
    qq = StringField()
    head_img = StringField(validators=[URL(message=u'头像格式不对！')])
    signature = StringField()


















