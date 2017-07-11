from datetime import datetime
from flask import render_template,session,redirect,url_for,abort,flash,request,send_from_directory,jsonify
from flask_login import login_required,current_user
from werkzeug import secure_filename
from . import main
from .forms import NameForm,EditProfileForm,PostForm
from .. import  db
from ..models import User,Post,Mblog
from ..model.blog import Blog
import os
import json
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
ALLOWED_EXTENSION = set(['png','jpeg','jpg','gif']);
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSION

@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page',type=int)
    pagination = Blog.query.filter_by(is_del=0).order_by(Blog.created_at.desc()).paginate(page,per_page=10,error_out=False)
    blogs = pagination.items
    if len(blogs)==0:
        abort(404)
    for blog in blogs:
        if blog.blog_body_short is None:
            BsObj = BeautifulSoup(blog.blog_body,'html.parser')
            blog.blog_body_short = BsObj.get_text()[0:300] if len(BsObj.get_text())>300 else BsObj.get_text()
            db.session.add(blog)
            db.session.commit()
    return render_template('index.html',pagination=pagination,blogs=blogs)

@main.route('/blog/<int:blog_id>')
def blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is None:
        abort(404)
    else:
        return render_template('blog.html',blog=blog)



#个人中心
@main.route('/user/<username>')
@login_required
def user(username):
    '''
        含参数变量
    :param name:
    :return:
    '''
    # return '<h1>Hello,%s!</h1>' % name
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts,hide_right=True)

#个人信息编辑
@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('你的个人信息已经更新')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form,hide_right=True)



@main.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extend = filename.rsplit('.',1)[1]
            filename = current_user.username + "_" + str(int(time.mktime(datetime.now().timetuple())))+"."+extend
            file.save(os.path.join(os.getcwd(),'uploads/'+filename))
            current_user.avatar = filename
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('.user',username=current_user.username))
    abort(500)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(),'uploads'),filename)

#关注用户
@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无此用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已经关注了此用户了')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('关注成功')
    return redirect(url_for('.user',username=username))
#取消关注
@main.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无此用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('你已经取消关注了')
        return redirect(url_for('.user',username=username))
    current_user.unfollow(user)
    flash('取消关注成功')
    return redirect(url_for('.user',username=username))

@main.route('/user/spider')
@login_required
def spider():
    '''
        只有我能看到 哈哈哈哈哈
    :return:
    '''
    if current_user.username != 'Lxiao':
        abort(404)
    page = request.args.get('page',1,type=int)
    pagination = Mblog.query.order_by(Mblog.id.asc()).paginate(page,per_page=20,error_out=False)
    blogs = pagination.items
    for blog in blogs:
        if blog.pics:
            blog.pics = json.loads(blog.pics)
        else:
            blog.pics = ''
    return render_template('spider.html',pagination=pagination,blogs=blogs,hide_right=True)