from . import admin
from .. import db
from flask_login import login_required
from flask import render_template
@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin.route('/login')
def login():
    return render_template('admin/login.html')