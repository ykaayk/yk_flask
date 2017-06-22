# coding:utf8

from wtforms import StringField, BooleanField, ValidationError, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from baseforms import BaseForm
from utils import xtcache


class CMSLoginForm(BaseForm):
    email = StringField(validators=[InputRequired(), Email(message=u'邮箱地址有误')])
    password = StringField(validators=[InputRequired(), Length(6, 20, message=u'密码长度必须在6-20个字符之间')])
    remember = BooleanField()


class CMSResetpwd(BaseForm):
    oldpwd = StringField(validators=[InputRequired(u'必须输入密码'), Length(6, 20, message=u'密码格式不正确')])
    newpwd = StringField(validators=[InputRequired(u'必须输入新密码'), Length(6, 20, message=u'新密码格式不正确')])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd', message=u'两次密码必须一致')])


class CMSResetmailForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'必须输入邮箱！'), Email(message=u'邮箱格式不满足！')])
    captcha = StringField(validators=[InputRequired(message=u'必须输入验证码!'), Length(4, 4, message=u'验证码错误')])

    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        captcha_cache = xtcache.get(email)
        if not captcha_cache or captcha_cache.lower() != captcha.lower():
            raise ValidationError(message=u'验证码错误')
        return True


class CMSAddUserForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'必须输入邮箱！'), Email(message=u'邮箱格式不满足！')])
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    password = StringField(validators=[InputRequired(message=u'必须输入密码！'), Length(6, 20, message=u'密码长度必须在6-20个字符之间！')])


class CMSBlackListForm(BaseForm):
    user_id = IntegerField(validators=[InputRequired(message=u'必须传入id!')])
    is_black = BooleanField(validators=[InputRequired(message=u'必须指定是或否加入黑名单！')])


class CMSBlackFrontUserForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'必须传入id!')])
    is_black = BooleanField(validators=[InputRequired(message=u'必须指定是或否加入黑名单！')])


class BoardForm(BaseForm):
    board_name = StringField(validators=[InputRequired(message=u'必须输出板块名称！'), Length(1, 20, message=u'板块名称不许在1-20个字符之间！')])


class EditBoardForm(BaseForm):
    board_id = StringField(validators=[InputRequired(message=u'必须传入id！')])
    board_name = StringField(validators=[InputRequired(message=u'必须输出板块名称！'), Length(1, 20, message=u'板块名称不许在1-20个字符之间！')])


class CMSHighLightPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须传入帖子id！')])
    is_highlight = BooleanField(validators=[InputRequired(message=u'必须传入行为！')])















