from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
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

class User(UserMixin,db.Model):
    '''
        定义users表的模型User
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True)

    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    #定义外键 ，话说外键也是 数据表的一个字段，别特殊化了
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

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

    def __repr__(self):
        return '<User %r>' % self.username
