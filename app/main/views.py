from datetime import datetime
from flask import render_template,session,redirect,url_for,abort,flash,request,send_from_directory
from flask_login import login_required,current_user
from werkzeug import secure_filename
from . import main
from .forms import NameForm,EditProfileForm,PostForm
from .. import  db
from ..models import User,Post
import os
from datetime import datetime
import time

ALLOWED_EXTENSION = set(['png','jpeg','jpg','gif']);
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSION

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.is_authenticated and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
    posts = pagination.items
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',form=form,pagination=pagination,posts=posts,current_time = datetime.utcnow())




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
