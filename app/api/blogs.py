from flask import jsonify,request,g,url_for,current_app
from .. import db
from ..model.blog import Blog
from . import  api

@api.route('/blogs')
def get_blogs():
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    blogs = [blog.to_json() for blog in blogs]
    return jsonify(blogs)