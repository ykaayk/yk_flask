# coding:utf8
import flask
from flask import Blueprint
from models.cmsmodels import CMSUser, CMSRole
from models.frontmodels import FrontUser
from models.commonmodels import BoardModel, PostModel, HighLightPostModel
from exts import db
from forms.cmsforms import CMSLoginForm, CMSResetpwd, CMSResetmailForm, CMSAddUserForm, CMSBlackListForm, \
    CMSBlackFrontUserForm, BoardForm, EditBoardForm, CMSHighLightPostForm
from constants import CMS_SESSION_ID
from decorators.cmsdecorators import login_required, superadmin_required
from utils import xtjson, xtmail
import random
import string
from utils import xtcache
from datetime import datetime
import constants

bp = Blueprint('cms', __name__, subdomain='cms')
# bp = Blueprint('cms', __name__, url_prefix='/cms')
# bp = Blueprint('cms', __name__)

# CMS首页
@bp.route('/')
@login_required
def index():
    return flask.render_template('cms/cms_index.html')
# 大部分html继承模板cms_base.html


# CMS后台用户登陆
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('cms/login.html')
    else:
        # html获得的form，传入验证表单，初始化
        form = CMSLoginForm(flask.request.form)
        # 验证表单格式/数据
        if form.validate():
            # 如果通过form验证
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            # 判断登陆用户是否在数据库已经存在
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                # 用户是否被拉黑
                if not user.is_active:
                    return flask.abort(401)
                # 用户存在数据库中, 处理完成后页面重定向到cms.index
                # 将用户信息保存在session中，确保已经登陆
                flask.session[CMS_SESSION_ID] = user.id
                if remember:    # 是否记住
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                # 最后登录时间
                user.last_login_time = datetime.now()
                db.session.commit()
                return flask.redirect(flask.url_for('cms.index'))
            else:
                # 用户不存在数据库中，则重新渲染并传入消息message
                return flask.render_template('cms/login.html', message=u'邮箱或密码错误')
        else:
            # 没通过form验证
            message = form.get_error()
            return flask.render_template('cms/login.html', message=message)


# CMS用户注销登录
@bp.route('/logout/')
@login_required
def logout():
    flask.session.pop(CMS_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))


# CMS个人中心
@bp.route('/profile/')
@login_required
def profile():
    return flask.render_template('cms/cms_profile.html')


# CMS用户修改密码
@bp.route('/resetpwd/', methods=['GET', 'POST'])
@login_required
def resetpwd():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetpwd.html')
    else:
        form = CMSResetpwd(flask.request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            if flask.g.cms_user.check_password(oldpwd):
                flask.g.cms_user.password = newpwd
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'原始密码错误')
        else:
            message = form.get_error()
            return xtjson.json_params_error(message=message)


# CMS用户修改邮箱
@bp.route('/resetmail/', methods=['GET', 'POST'])
@login_required
def resetmail():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetmail.html')
    else:
        form = CMSResetmailForm(flask.request.form)
        if form.validate():
            email = form.email.data
            if flask.g.cms_user.email == email:
                return xtjson.json_params_error(message=u'新邮箱与旧邮箱一致，无需求修改！')
            flask.g.cms_user.email = email
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 实现 验证码通过e-mail发送
@bp.route('/mail_captcha/')
@login_required
def mail_captcha():
    # mail_captcha/xxxx@qq.com/
    # 查询字符串 /mail_captcha/?email=xxx@qq.com
    email = flask.request.args.get('email')

    if xtcache.get(email):
        return xtjson.json_params_error(message=u'该邮箱已经发送验证码了！')

    source = list(string.letters)
    for x in xrange(0, 10):
        source.append(str(x))
    captcha_list = random.sample(source, 4)
    captcha = ''.join(captcha_list)

    if xtmail.send_mail(subject=u'周杰伦发来的邮箱验证码', receivers=email, body=u'邮箱验证码是：'+captcha):
        # 为了下次可以验证邮箱和验证码
        # 为了防止用户不断的刷新这个接口
        xtcache.set(email, captcha)
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=u'服务器错误')

# 发送html格式的内容的邮件
# @bp.route('/test/')
# def test():
#     html = flask.render_template('cms_test.html')
#     ykmail.send_mail(subject=u'test', receivers='ykssyk@qq.com', html=html)
#     return 'success'


# CMS用户管理
@bp.route('/cmsusers/')
@login_required
@superadmin_required
def cmsusers():
    users = CMSUser.query.all()
    context = {
        'users': users
    }
    return flask.render_template('cms/cms_cmsusers.html', **context)


# CMS用户管理：实现 新增CMS用户
@bp.route('/add_cmsuser/', methods=['GET', 'POST'])
@login_required
@superadmin_required
def add_cmsuser():
    if flask.request.method == 'GET':
        roles = CMSRole.query.all()
        context = {
            'roles': roles
        }
        return flask.render_template('cms/cms_addcmsuser.html', **context)
    else:
        form = CMSAddUserForm(flask.request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            roles = flask.request.form.getlist('roles[]')
            if not roles:
                return xtjson.json_params_error(message=u'必须制定最少一个分组！')

            user = CMSUser(email=email, username=username, password=password)
            for role_id in roles:
                role = CMSRole.query.get(role_id)
                role.users.append(user)
                # user.roles.append(role)
            # db.session.add(user)
            # 先 user.roles.append(role)，再 db.session.add(user)。因为user没有添加到数据库
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# CMS用户管理：实现 管理、编辑CMS用户
@bp.route('/edit_cmsuser/', methods=['GET', 'POST'])
@login_required
@superadmin_required
def edit_cmsuser():
    # 两种获取数据的方法
    # /edit_cmsuser/?user_id=xxxx
    # /edit_cmsuser/xxxxx/
    if flask.request.method == 'GET':
        user_id = flask.request.args.get('user_id')
        if not user_id:
            # 错误处理；后续要写相关页面
            flask.abort(404)
        user = CMSUser.query.get(user_id)
        roles = CMSRole.query.all()
        current_roles = [role.id for role in user.roles]
        context = {
            'user': user,
            'roles': roles,
            'current_roles': current_roles  # 存储当前用户所有的角色id
        }
        return flask.render_template('cms/cms_editcmsuser.html', **context)
    else:
        user_id = flask.request.form.get('user_id')
        roles = flask.request.form.getlist('roles[]')  # 获取列表
        if not user_id:
            return xtjson.json_params_error(message=u'没有指定id！')
        if not roles:
            return xtjson.json_params_error(message=u'必须指定一个角色分组！')

        user = CMSUser.query.get(user_id)
        # 清掉之前的角色信息
        user.roles[:] = []
        # 添加新的角色
        for role_id in roles:
            role_model = CMSRole.query.get(role_id)
            user.roles.append(role_model)
        db.session.commit()
        return xtjson.json_result()


# CMS用户管理：实现 拉黑
@bp.route('/black_list/', methods=['POST'])
@login_required
@superadmin_required
def black_list():
    form = CMSBlackListForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        if user_id == flask.g.cms_user.id:
            return xtjson.json_params_error(message=u'不能修改自己')
        is_active = form.is_black.data  # 布尔类型
        user = CMSUser.query.get(user_id)
        user.is_active = not is_active
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# CMS：管理前台用户
@bp.route('/front_users/')
@login_required
def front_users():
    sort = flask.request.args.get('sort')
    front = None
    if not sort or sort == '1':  # 按加入时间排序
        front = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    else:
        front = FrontUser.query.order_by(FrontUser.telephone.desc()).all()

    # elif sort == '2':  # 按帖子数量排序
    #     pass
    # elif sort == '3':  # 按评论数量排序
    #     pass

    context = {
        'front_users': front,
        'current_sort': sort,
    }
    return flask.render_template('cms/cms_frontusers.html', **context)


# 编辑前端用户：展示和拉黑
@bp.route('/edit_frontuser/')
@login_required
def edit_frontuser():

    user_id = flask.request.args.get('id')
    if not user_id:
        flask.abort(404)

    user = FrontUser.query.get(user_id)
    if not user:
        flask.abort(404)

    return flask.render_template('cms/cms_editfrontusers.html', current_user=user)


# 实现CMS用户拉黑前端用户
@bp.route('/black_front_user/', methods=['POST'])
@login_required
def black_front_user():
    form = CMSBlackFrontUserForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        is_black = form.is_black.data
        user = FrontUser.query.get(user_id)
        if not user:
            return flask.abort(404)
        # 这样一样实现
        # if user.is_active:
        #     user.is_active = False
        # else:
        #     user.is_active = True
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 板块管理
@bp.route('/boards/')
@login_required
def boards():
    all_boards = BoardModel.query.order_by(BoardModel.create_time.desc()).all()
    context = {
        'boards': all_boards
    }
    return flask.render_template('cms/cms_boards.html', **context)


# 添加板块
@bp.route('/add_board/', methods=['POST'])
@login_required
def add_board():
    form = BoardForm(flask.request.form)
    if form.validate():
        name = form.board_name.data
        author_id = flask.g.cms_user.id
        if BoardModel.query.filter(BoardModel.name == name).first():
            # print u'板块名称重复'
            return xtjson.json_params_error(message=u'板块名称重复')
        a_board = BoardModel(name=name, author_id=author_id)
        db.session.add(a_board)
        db.session.commit()
        return xtjson.json_result()


# 编辑板块名称
@bp.route('/edit_board/', methods=['POST'])
@login_required
def edit_board():
    form = EditBoardForm(flask.request.form)
    if form.validate():
        board_id = form.board_id.data
        board_name = form.board_name.data
        if BoardModel.query.filter(BoardModel.name == board_name).first():
            return xtjson.json_params_error(message=u'板块名称已存在！')

        a_board = BoardModel.query.get(board_id)
        a_board.name = board_name
        db.session.commit()
        return xtjson.json_result()


# 删除板块
@bp.route('/del_board/', methods=['POST'])
@login_required
def del_board():
    board_id = flask.request.form.get('board_id')
    board = BoardModel.query.get(board_id)
    if not board_id and board:
        return xtjson.json_params_error(message=u'出错了！！')
    if board.posts:
        return xtjson.json_params_error(message=u'此板块存在帖子，不能删除！')
    db.session.delete(board)
    db.session.commit()
    return xtjson.json_result()


# 帖子管理
@bp.route('/posts/')
@login_required
def posts():
    # 排序方式，查询字符串: / /
    sort_board = flask.request.args.get('board', 0, type=int)  # 0 所有板块的帖子， 1、2....板块的帖子
    sort_type = flask.request.args.get('sort', 1, type=int)  # 1 按时间，2 按加精顺序，3 评论量
    sort_forbid = flask.request.args.get('forbid', 0, type=int)  # 0 显示所 有帖子，1 仅显示正常帖子，2 仅显示禁用帖子

    # 默认显示是：0 所有板块的帖子/ 1 按时间/ 0 所有帖子
    posts_p = []

    # sort_board == 0 所有板块
    if sort_board == 0:

        # 按时间
        if sort_type == 1:

            # 仅显示正常的帖子
            if sort_forbid == 1:
                # 所有板块0 按时间1 显示正常1
                posts_p = PostModel.query.filter_by(is_removed=False).order_by(PostModel.create_time.desc()).all()

            # 仅显示禁用的帖子
            elif sort_forbid == 2:
                # 所有板块0 按时间1 显示禁用2
                posts_p = PostModel.query.filter_by(is_removed=True).order_by(PostModel.create_time.desc()).all()

            # 全部显示
            else:
                # 所有板块0 按时间1 全部显示0
                posts_p = PostModel.query.order_by(PostModel.create_time.desc()).all()

        # 按加精顺序
        elif sort_type == 2:

            # 仅显示正常的帖子
            if sort_forbid == 1:
                # 所有板块0 按加精顺序2 显示正常1
                posts_p = db.session.query(PostModel).outerjoin(HighLightPostModel).filter(PostModel.is_removed == False).order_by(
                    HighLightPostModel.create_time.desc(), PostModel.create_time.desc()).all()

            # 仅显示禁用的帖子
            elif sort_forbid == 2:
                # 所有板块0 按加精顺序2 显示禁用2
                # 加入两个条件 HighLightPostModel.create_time.desc(), PostModel.create_time.desc()
                posts_p = db.session.query(PostModel).outerjoin(HighLightPostModel).filter(PostModel.is_removed == True).order_by(
                    HighLightPostModel.create_time.desc())

            # 全部显示
            else:
                # 所有板块0 按加精顺序2 全部显示0
                posts_p = db.session.query(PostModel).outerjoin(HighLightPostModel).order_by(
                    # HighLightPostModel.create_time.desc()).all()
                    HighLightPostModel.create_time.desc(), PostModel.create_time.desc()).all()

        # 按评论量
        elif sort_type == 3:
            # 未实现
            posts_p = PostModel.query.order_by(PostModel.create_time.desc()).all()

    # 按板块id，sort_board
    else:

        # 按时间
        if sort_type == 1:

            # 仅显示正常的帖子
            if sort_forbid == 1:
                # 板块id 按时间1 显示正常1
                # posts_p = PostModel.query.filter(PostModel.is_removed == False, PostModel.board_id
                posts_p = PostModel.query.filter(PostModel.is_removed == False).filter(PostModel.board_id
                                                                                       == sort_board).order_by(PostModel.create_time.desc()).all()

            # 仅显示禁用的帖子
            elif sort_forbid == 2:
                # 板块id 按时间1 显示禁用2
                # posts_p = PostModel.query.filter(PostModel.is_removed == True, PostModel.board_id
                posts_p = PostModel.query.filter(PostModel.is_removed == True, PostModel.board_id
                                                 == sort_board).order_by(PostModel.create_time.desc()).all()

            # 全部显示
            else:
                # 板块id 按时间1 全部显示0
                # posts_p = PostModel.query.filter(PostModel.board_id
                posts_p = PostModel.query.filter(PostModel.board_id
                                                 == sort_board).order_by(PostModel.create_time.desc()).all()

        # 按加精顺序
        elif sort_type == 2:

            # 仅显示正常的帖子
            if sort_forbid == 1:
                # 板块id 按加精顺序2 显示正常1
                posts_p = db.session.query(PostModel).outerjoin(HighLightPostModel).filter(
                    # PostModel.board.id == sort_board, PostModel.is_removed == False).order_by(
                    PostModel.board_id == sort_board, PostModel.is_removed == False).order_by(
                    HighLightPostModel.create_time.desc(), PostModel.create_time.desc()).all()

            # 仅显示禁用的帖子
            elif sort_forbid == 2:
                # 板块id 按加精顺序2 显示禁用2
                posts_p = db.session.query(PostModel).outerjoin(HighLightPostModel).filter(
                    # PostModel.board.id == sort_board, PostModel.is_removed == True).order_by(
                    PostModel.board_id == sort_board, PostModel.is_removed == True).order_by(
                    HighLightPostModel.create_time.desc(), PostModel.create_time.desc()).all()

            # 全部显示
            else:
                # 板块id 按加精顺序2 全部显示0
                posts_p = db.session.query(PostModel).outerjoin(HighLightPostModel).filter(
                    # PostModel.board.id == sort_board).order_by(
                    PostModel.board_id == sort_board).order_by(
                    HighLightPostModel.create_time.desc(), PostModel.create_time.desc()).all()

        # 按评论量
        elif sort_type == 3:
            # 未实现
            posts_p = PostModel.query.order_by(PostModel.create_time.desc()).all()

    # PostModel.query.filter(PostModel.xx == xx)/   PostModel.query.filter_by(xx=xx)

    # 帖子总数
    posts_num = len(posts_p)
    # 总页码
    if posts_num % constants.PAGE_NUM_BACK != 0:
        posts_page = posts_num / constants.PAGE_NUM_BACK + 1
    else:
        posts_page = posts_num / constants.PAGE_NUM_BACK
    # 当前页码, 默认1
    current_page = flask.request.args.get('current_page', 1, int)
    if current_page > posts_page:
        current_page = posts_page
    if current_page <= 0:
        current_page = 1
    # print 'current_page:', current_page

    # 10页一翻页 / N页
    N = 10
    # 开始页码 结束页码
    # 第一种
    p = current_page / N
    q = current_page % N
    if q != 0:
        end_page_num = (p+1)*N
        start_page_num = end_page_num - N + 1
    else:
        end_page_num = p*N
        start_page_num = end_page_num - 9
    if end_page_num > posts_page:
        end_page_num = posts_page

    # 第二种
    # start_page_num = current_page / N * N + 1
    # if start_page_num > current_page:
    #     start_page_num -= N
    # end_page_num = start_page_num + N - 1
    # if end_page_num > posts_page:
    #     end_page_num = posts_page

    # 页码，用列表传递
    pages = range(start_page_num, end_page_num+1)
    # 本页码 第一篇帖子序列
    start_post = (current_page-1) * constants.PAGE_NUM_BACK + 1
    # 在此页码的帖子的序列1-15，16-30, 31-45...（PAGE_NUM=15)
    # 如果本页第一篇序列+（15-1）即本页最后一篇post序号大于帖子总数，则总帖子的最后一贴 就是 本页最后一贴
    # 如果总帖子26，则第2页，在此页码的帖子的序列：16-26
    # 否则本页最后一贴就是 第一篇+（15-1）（PAGE_NUM=15）
    # print posts_num
    if start_post + (constants.PAGE_NUM_BACK-1) > posts_num:
        end_post = posts_num
    else:
        end_post = start_post + (constants.PAGE_NUM_BACK-1)

    boards_p = BoardModel.query.all()
    context = {
        'boards': boards_p,
        'posts': posts_p[start_post-1: end_post],
        'sort_type': sort_type,
        'sort_board': sort_board,
        'sort_forbid': sort_forbid,
        'current_page': current_page,
        'posts_page': posts_page,
        'pages': pages
    }
    return flask.render_template('cms/cms_posts.html', **context)


# 帖子加精
@bp.route('/highlight/', methods=['POST'])
@login_required
def highlight():
    form = CMSHighLightPostForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data  # 加精的帖子id
        is_highlight = form.is_highlight.data  # 传入参数：是否加精
        post_model = PostModel.query.get(post_id)  # 从数据库中获取需要加精的帖子
        if is_highlight:
            if post_model.highlight:
                return xtjson.json_params_error(message=u'该帖子已经加精！')
            highlight_model = HighLightPostModel()
            post_model.highlight = highlight_model
            db.session.commit()
            db.session.close()
            return xtjson.json_result()
        else:
            if not post_model.highlight:
                return xtjson.json_params_error(message=u'该帖子已经取消加精！')
            db.session.delete(post_model.highlight)
            db.session.commit()
            db.session.close()
            return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 帖子移除/删除
@bp.route('/post_remove/', methods=['POST'])
@login_required
def post_remove():
    post_id = flask.request.form.get('post_id')
    is_removed = flask.request.form.get('is_removed')  # unicode编码
    if not post_id:
        return xtjson.json_params_error(message=u'必须输入帖子id！')
    post_model = PostModel.query.get(post_id)
    if post_model.is_removed:
        post_model.is_removed = False
    else:
        post_model.is_removed = True
    db.session.commit()
    db.session.close()
    return xtjson.json_result()


# # 钩子函数：请求之前执行，判断是否已经登陆
# @bp.before_request
# def cms_before_request():
#     id = flask.session.get(CMS_SESSION_ID)
#     if id:
#         user = CMSUser.query.get(id)
#         flask.g.cms_user = user


# # 上下文处理器
# # 钩子函数：返回一个字典
# @bp.context_processor
# def cms_context_processor():
#     id = flask.session.get(CMS_SESSION_ID)
#     if id:
#         user = flask.g.cms_user
#         return {'cms_user': user}
#     else:
#         return {}


# 404错误页面的视图函数
@bp.errorhandler(404)
def cms_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return flask.render_template('cms/cms_404.html'), 404


# 401错误页面的视图函数
@bp.errorhandler(401)
def cms_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.render_template('cms/cms_401.html'), 401

# 测试代码

# 添加用户
# @bp.route('/test_create_user/')
# def test():
#     user = CMSUser(email='xx@qq.com', password='xxx', username='xxxx')
#     db.session.add(user)
#     db.session.commit()
#     return '添加用户成功'


# 密码加密
# @bp.route('/test_pwd/')
# def test():
#     pwd = '111111'
#     hashed_pwd = generate_password_hash(pwd)
#     print hashed_pwd
#     return str(check_password_hash(hashed_pwd, pwd))

# 发送邮件
# @bp.route('/test_mail/')
# def mail():
#     mail = Mail(flask.current_app)
#     message = Message(subject=u'周杰伦发来的一封邮件', recipients=['ykssyk@qq.com'], body='asdf')
#     mail.send(message)
#     return 'success!'


