from .. import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from ..models import User
from .. import login_manager
from time import time
from datetime import datetime

from datetime import datetime


class Blog_Type(db.Model):
    __tablename__ = 'blog_type'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True)
    blogs = db.relationship('Blog',backref='btype',lazy="dynamic")

    def __repr__(self):
        return '<Blog_Type {0}>'.format(self.name)
class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    btype_id = db.Column(db.Integer,db.ForeignKey('blog_type.id'))
    blog_body = db.Column(db.Text)
    tags = db.Column(db.String(255))
    is_show_all = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    update_at = db.Column(db.DateTime,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Blog 《{0}》by:{1}>'.format(self.title,self.author.username)