from datetime import datetime
from flask import render_template,session,redirect,url_for
from flask_login import login_required
from . import main
from .forms import NameForm
from .. import  db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'),current_time = datetime.utcnow(),known=session.get('known'))

@main.route('/user/<name>')
@login_required
def user(name):
    '''
        含参数变量
    :param name:
    :return:
    '''
    # return '<h1>Hello,%s!</h1>' % name
    return render_template('user.html',name=name)

@main.route('/redirect')
def redit():
    '''
        跳转
    :return:
    '''
    return redirect('http://www.baidu.com')
