# coding:utf8

from exts import db
from sbbs import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import commonmodels, frontmodels, cmsmodels


CMSUser = cmsmodels.CMSUser
CMSRole = cmsmodels.CMSRole
CMSPermission = cmsmodels.CMSPermission

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# 添加CMS用户
# @manager.option('-e', '--email', dest='email')
# @manager.option('-u', '--username', dest='username')
# @manager.option('-p', '--password', dest='password')
# def create_cms_user(email, username, password):
#     user = CMSUser.query.filter_by(email=email).first()
#     if user:
#         return u'该邮箱已经存在！'
#     else:
#         user = CMSUser(email=email, username=username, password=password)
#         db.session.add(user)
#         db.session.commit()
#         print u'添加CMS用户成功'


# 添加CMS角色(权限)
@manager.option('-n', '--name', dest='name')
@manager.option('-d', '--desc', dest='desc')
@manager.option('-p', '--permissions', dest='permissions')
def create_role(name, desc, permissions):
#    role = CMSRole(name=name.decode('gbk').encode('utf8'), desc=desc.decode('gbk').encode('utf8'), permissions=permissions.decode('gbk').encode('utf8'))
    role = CMSRole(name=name.decode('utf8'), desc=desc.decode('utf8'), permissions=permissions.decode('utf8'))
    db.session.add(role)
    db.session.commit()
    print u'恭喜！角色添加成功！'


# 添加用户的角色(权限)
@manager.option('-e', '--email', dest='email')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-r', '--role_name', dest='role')
def create_cms_user(email, username, password, role):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        print u'邮箱已经存在！'
        return
#    roleModel = CMSRole.query.filter_by(name=role.decode('gbk').encode('utf8')).first()
    roleModel = CMSRole.query.filter_by(name=role.decode('utf8')).first()
    if not roleModel:
        print u'角色不存在！'
        return
    user = CMSUser(username=username, password=password, email=email)
    roleModel.users.append(user)
    db.session.commit()
    print u'恭喜！CMS用户添加成功！'


if __name__ == '__main__':
    manager.run()






















