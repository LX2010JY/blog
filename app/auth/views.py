from flask import render_template,flash,redirect,url_for,request
from flask_login import logout_user,login_required,login_user
from . import auth
from .forms import LoginForm,RegistretionForm
from ..models import User
from .. import db

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User.query.filter_by(username=form.email.data).first()
        if user is not None and  user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('用户名或密码错误.')
    return render_template('auth/login.html',form=form,hide_right=True)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/change_password')
@login_required
def change_password():
    pass

@auth.route('/change_email_request')
@login_required
def change_email_request():
    pass


@auth.route('/register',methods=['POST','GET'])
@login_required
def register():
    form = RegistretionForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('现在你可以去登录了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form,hide_right=True)