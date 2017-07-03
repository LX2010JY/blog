from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from time import time
from datetime import datetime
#定义数据表模型 （难）
class Role(db.Model):
    '''
        定义数据表roles的模型Role(注意：一个是复数，一个是单数，不要混了)
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    #这里定义user和role的关系，调用users可以获取在这个角色下所有相关的user信息
    #话说外键不是不能用的吗
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r' % self.name
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class User(UserMixin,db.Model):
    '''
        定义users表的模型User
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True)
    avatar = db.Column(db.String(64),unique=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())

    member_since = db.Column(db.DateTime(),default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)

    #定义外键 ，话说外键也是 数据表的一个字段，别特殊化了
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    posts = db.relationship('Post',backref='author',lazy='dynamic')
    #关注了哪些人
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],backref=db.backref('follower',lazy='joined'),lazy='dynamic',cascade='all,delete-orphan')
    #那些人关注了我
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],backref=db.backref('followed',lazy='joined'),lazy='dynamic',cascade='all,delete-orphan')
    @property
    def password(self):
        raise AttributeError('密码是不可读取的属性')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #加载用户回调函数
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    #关注某人
    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.session.commit()
    #取消关注
    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()
    #是否关注了某某某
    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None
    #是否被某某某关注
    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
class Mblog(db.Model):
    __tablename__ = 'mblog'
    id = db.Column(db.Integer,primary_key=True)
    m_id = db.Column(db.String(20),index=True)
    text = db.Column(db.Text)
    pics = db.Column(db.Text)
    thumbnail_pic = db.Column(db.Text)
    bmiddle_pic = db.Column(db.Text)
    original_pic = db.Column(db.Text)
    created_at = db.Column(db.String(20))
    


