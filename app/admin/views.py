from . import admin
from .. import db
from ..model.blog import Blog
from ..main.errors import page_not_found,internal_server_error
import os,json
from werkzeug import secure_filename
from flask_login import login_required,current_user
from flask import render_template,request,url_for,abort,flash,redirect
from datetime import datetime
import time
from bs4 import BeautifulSoup
ALLOWED_EXTENSION = set(['png','jpeg','jpg','gif']);
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSION

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html',type=1)

@admin.route('/upd/blog/<int:id>')
@login_required
def update_blog(id=0):
    blog = Blog.query.filter_by(id=id).first()
    if blog is None:
        abort(404)
    else:
        return render_template('admin/index.html',type=1,blog=blog)


@admin.route('/blogs')
@login_required
def blogs():
    page = request.args.get('page',1,type=int)
    pagination = Blog.query.filter_by(is_del=0).order_by(Blog.created_at.desc()).paginate(page,per_page=10,error_out=False)
    list = pagination.items
    xh = 0
    for item in list:
        xh+=1
        item.xh = xh
    return render_template('admin/blogs.html',pagination=pagination,list=list,type=2)


@admin.route('/login')
def login():
    return render_template('admin/login.html')

@admin.route('/uploadpic',methods=['GET','POST'])
@login_required
def uploadpic():
    if request.method == 'POST':
        file = request.files['fileData']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extend = filename.rsplit('.',1)[1]
            filename = 'blog_'+current_user.username + "_" + str(int(time.mktime(datetime.now().timetuple())))+"."+extend
            file.save(os.path.join(os.getcwd(),'uploads/'+filename))
            res = {
                'success' : True,
                'msg' : '上传成功',
                'file_path' : url_for('main.uploaded_file',filename=filename)
            }
            return json.dumps(res)
    abort(500)

@admin.route('/addblog',methods=['GET','POST'])
@login_required
def addblog():
    title = request.values.get('title')
    btype = request.values.get('btype')
    blog_body = request.values.get('blog_body')
    BsObj = BeautifulSoup(blog_body,'html.parser')
    blog_body_short = BsObj.get_text()[0:300] if len(BsObj.get_text())>300 else blog_body
    tags = request.values.get('tags')
    is_show_all = request.values.get('is_show_all')
    if title is None:
        title = '无标题文章'
    try:
        blog = Blog(title=title,btype_id=1,author_id=current_user.id,is_show_all=is_show_all,tags=tags,blog_body=blog_body,blog_body_short=blog_body_short)
        db.session.add(blog)
        db.session.commit()
        flash('文章发布成功')
    except:
        flash('文章发布失败了~~节哀')

    return redirect(url_for('admin.blogs'))

@admin.route('/updblog/<int:id>',methods=['GET','POST'])
@login_required
def updblog(id):
    title = request.values.get('title')
    btype = request.values.get('btype')
    blog_body = request.values.get('blog_body')
    BsObj = BeautifulSoup(blog_body,'html.parser')
    blog_body_short = BsObj.get_text()[0:300] if len(BsObj.get_text())>300 else blog_body
    tags = request.values.get('tags')
    is_show_all = request.values.get('is_show_all')
    if title is None:
        title = '无标题文章'
    try:
        blog = Blog.query.filter_by(id=id).first()
        if blog is None:
            blog = Blog(title=title,btype_id=1,author_id=current_user.id,is_show_all=is_show_all,tags=tags,blog_body=blog_body,blog_body_short=blog_body_short)
            db.session.add(blog)
            db.session.commit()
            flash('文章发布成功')
        else:
            blog.title = title
            blog.is_show_all = is_show_all
            blog.tags = tags
            blog.blog_body = blog_body
            blog.blog_body_short = blog_body_short
            blog.update_at = datetime.utcnow()
            db.session.add(blog)
            db.session.commit()
            flash('文章修改成功')
    except:
        flash('文章修改失败了~~节哀')

    return redirect(url_for('admin.blogs'))

@admin.route('/delblog',methods=['post'])
@login_required
def delblog():
    id = request.values.get('id')
    blog = Blog.query.filter_by(id=id).first()
    blog.is_del = 1
    db.session.add(blog)
    db.session.commit()
    return 'ok'