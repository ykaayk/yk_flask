# coding:utf8
import os

DB_USERNAME = 'yk'
DB_PASSWORD = 'yk123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'sbbs'


DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = 'ykaayk.club'


SECRET_KEY = os.urandom(24)

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式加密
MAIL_USERNAME = 'ykaayk@qq.com'
MAIL_PASSWORD = 'xoxhhiwshhaebhih'
MAIL_DEFAULT_SENDER = 'ykaayk@qq.com'
# MAIL_USE_SSL
# MAIL_DEBUG
# MAIL_MAX_EMAILS
# MAIL_SUPPRESS_SEND
# MAIL_ASCII_ATTACHMENTS








