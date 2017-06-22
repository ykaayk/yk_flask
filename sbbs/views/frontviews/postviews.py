# coding:utf8
from flask import Blueprint
import flask
from models.commonmodels import BoardModel, PostModel, CommentModel, PostStarModel, HighLightPostModel
from constants import SECRET_KEY, ACCESS_KEY, PAGE_NUM
from utils import xtjson
from forms.frontforms import AddPostForm, AddCommentForm, AddReply, StarPostForm
from decorators.frontdecorators import login_required
from exts import db
import qiniu
import settings
# from datetime import datetime
# from models.frontmodels import FrontUser
# from constants import FRONT_SESSION_ID


# 蓝图
# 首页
bp = Blueprint('post', __name__)


# 首页
@bp.route('/')
def index():
    return post_list(1, 2, 0)


# 帖子列表页，分页
@bp.route('/list/<page>/<sort_type>/<board_id>')
def post_list(page, sort_type, board_id):
    try:
        page = int(page)
        sort_type = int(sort_type)
        board_id = int(board_id)
    except:
        return flask.abort(404)
    # sort_type，1是最新，2是精华，3是点赞，4是评论
    if sort_type == 1:
        all_posts = PostModel.query.filter_by(is_removed=False).order_by(PostModel.create_time.desc())
    elif sort_type == 2:
        all_posts = db.session.query(PostModel).outerjoin(HighLightPostModel).filter(
            PostModel.is_removed == False).order_by(HighLightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort_type == 3:
        all_posts = db.session.query(PostModel).outerjoin(PostStarModel).group_by(PostModel.id).filter(
            PostModel.is_removed == False).order_by(db.func.count(PostModel.stars).desc(), PostModel.create_time.desc())
    elif sort_type == 4:
        all_posts = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).filter(
            PostModel.is_removed == False).order_by(db.func.count(PostModel.comments).desc(), PostModel.create_time.desc())
    else:
        all_posts = PostModel.query.filter_by(is_removed=False).order_by(PostModel.create_time.desc())

    if board_id:
        all_posts = all_posts.filter(PostModel.board_id == board_id).all()
    else:
        all_posts = all_posts.all()

    # page是从1开始的
    start = (page-1) * PAGE_NUM
    end = page * PAGE_NUM
    if len(all_posts) == 0:
        start = 1
        pass
    elif start >= len(all_posts):
        return flask.redirect('/')
    posts = all_posts[start:end]
    page_n = len(all_posts) % PAGE_NUM
    last_page = len(all_posts)/PAGE_NUM+1 if page_n else len(all_posts)/PAGE_NUM
    context = {
        'posts': posts,
        'posts_total': PostModel.query.filter_by(is_removed=False).all(),
        'boards': BoardModel.query.all(),
        'start_page': page,
        'last_page': last_page,
        'sort_type': sort_type,
        'board_id': board_id,
    }

    return flask.render_template('front/front_index.html', **context)


# 写新帖子
@bp.route('/add_post/', methods=['GET', 'POST'])
@login_required
def add_post():
    if flask.request.method == 'GET':
        boards = BoardModel.query.all()
        return flask.render_template('front/front_addpost.html', boards=boards)
    else:
        form = AddPostForm(flask.request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post_model = PostModel(title=title, content=content)
            # board_model = BoardModel.query.get(board_id).first()
            # board_model = BoardModel.query.filter(BoardModel.id == board_id).first()
            board_model = BoardModel.query.filter_by(id=board_id).first()
            if not board_model:
                return xtjson.json_params_error(message=u'没有该模板！')
            post_model.board = board_model
            post_model.author = flask.g.front_user
            # 写帖子积分+2
            post_model.author.points += 2

            db.session.add(post_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 七牛
@bp.route('/qiniu_token/')
def qiniu_token():
    # 授权
    q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)

    # 选择七牛的云空间
    bucket_name = 'ykvideo'

    # 生成许可证token
    token = q.upload_token(bucket_name)

    return flask.jsonify({'uptoken': token})


# 帖子详情页
@bp.route('/post_detail/<int:post_id>/')
def post_detail(post_id):
    post_model = PostModel.query.get(post_id)
    if not post_model:
        return flask.abort(404)
    if post_model.is_removed:
        return flask.abort(404)
    # 这篇帖子的点赞的用户
    star_user_ids = [star.author.id for star in post_model.stars]
    star_users = [star.author for star in post_model.stars]
    context = {
        'post': post_model,
        'star_user_ids': star_user_ids,
        'star_users': star_users
    }
    return flask.render_template('front/front_postdetail.html', **context)


# 计时器，计算阅读数
@bp.route('/read_time/', methods=['POST'])
def read_time():
    read_num = flask.request.form.get('read_num')
    post_id = flask.request.form.get('post_id')
    read_num = int(read_num)
    if read_num == 1:
        PostModel.query.get(post_id).read_count += 1
        db.session.commit()
    return xtjson.json_result()


# 添加帖子评论
@bp.route('/add_comment/', methods=['GET', 'POST'])
@login_required
def add_comment():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('post_id')
        post_model = PostModel.query.get(post_id)
        return flask.render_template('front/front_addcoment.html', post=post_model)
    else:
        if flask.g.front_user.points < settings.COMMENT_ALLOW_POINTS:
            message = u'你的积分是%s，少于评论需求的%s积分，去发布帖子、写评论和做任务' \
                      u'挣积分吧~' % (flask.g.front_user.points, settings.COMMENT_ALLOW_POINTS)
            return xtjson.json_params_error(message=message)
        form = AddCommentForm(flask.request.form)
        if form.validate():
            post_id = form.post_id.data
            content = form.content.data
            comment_model = CommentModel(content=content)
            post_model = PostModel.query.get(post_id)
            comment_model.post = post_model
            comment_model.author = flask.g.front_user
            # 评论积分+1
            comment_model.author.points += 1
            db.session.add(comment_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 添加子评论
@bp.route('/comment_reply/', methods=['POST'])
@login_required
def comment_reply():
    form = AddReply(flask.request.form)
    if form.validate():
        comment_id = form.comment_id.data
        reply = form.reply.data
        comment_model = CommentModel.query.get(comment_id)
        reply_model = CommentModel(content=reply)
        reply_model.author = flask.g.front_user
        reply_model.origin_comment = comment_model
        db.session.add(reply_model)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_method_error(message=u'bug!!')


# 帖子点赞
@bp.route('/post_star/', methods=['POST'])
@login_required
def post_star():
    form = StarPostForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data

        post_model = PostModel.query.get(post_id)
        star_model = PostStarModel.query.filter_by(author_id=flask.g.front_user.id, post_id=post_id).first()
        if star_model:
            if is_star:
                db.session.delete(star_model)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'点赞bug请刷新！')
        else:
            if not is_star:
                # 这三种添加model都可以
                # 1 外键id
                # star_model = PostStarModel(author_id=flask.g.front_user.id, post_id=post_id)
                # 2 外键对象
                star_model = PostStarModel(author=flask.g.front_user, post=post_model)
                # 3 先建立modle，再给外键对象
                # star_model = PostStarModel()
                # star_model.author = flask.g.front_user
                # star_model.post = post_model

                db.session.add(star_model)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'点赞bug请刷新！')
    else:
        return xtjson.json_params_error(message=form.get_error())


# # 请求之前执行，若已登陆，则将用户存入flask.g.front_user中
# @bp.before_request
# def front_before_request():
#     front_user_id = flask.session.get(FRONT_SESSION_ID)
#     if front_user_id:
#         front_user = FrontUser.query.get(front_user_id)
#         flask.g.front_user = front_user


# # 验证是否登录，若登录了则返回front_user给模板渲染使用
# # 供模板渲染随时使用
# @bp.context_processor
# def post_context_processor():
#     id = flask.session.get(FRONT_SESSION_ID)
#     if id:
#         front_user = flask.g.front_user
#         return {'front_user': front_user}
#     else:
#         return {}

# 401
# @bp.errorhandler(401)
# def post_auth_forbindden(error):
#     if flask.request.is_xhr:
#         return xtjson.json_unauth_error()
#     else:
#         return flask.redirect(flask.url_for('account.login'))


# 写入N遍测试帖子
# @bp.route('/test/')
# def test():
#     author = FrontUser.query.first()
#     board = BoardModel.query.first()
#     for x in range(15):
#         title = '帖子标题：%s' % x
#         content = '帖子内容：%s' % x
#         post_model = PostModel(title=title, content=content)
#         post_model.author = author
#         post_model.board = board
#         db.session.add(post_model)
#     db.session.commit()
#     return 'success!'


# # 404错误页面的视图函数
# @bp.errorhandler(404)
# def cms_not_found(error):
#     if flask.request.is_xhr:
#         return xtjson.json_params_error()
#     else:
#         return flask.render_template('cms/cms_404.html'), 404




