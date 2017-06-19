from datetime import datetime
from flask import render_template,session,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from . import main
from .forms import NameForm,EditProfileForm,PostForm
from .. import  db
from ..models import User,Post

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.is_authenticated and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',form=form,posts=posts,current_time = datetime.utcnow())

# @main.route('/',methods=['GET','POST'])
# def _index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             db.session.commit()
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('main.index'))
#     return render_template('2_index.html', form=form, name=session.get('name'),current_time = datetime.utcnow(),known=session.get('known'))

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
    return render_template('user.html',user=user,posts=posts)

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
    return render_template('edit_profile.html',form=form)




@main.route('/redirect')
def redit():
    '''
        跳转
    :return:
    '''
    return redirect('http://www.baidu.com')
