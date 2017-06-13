from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from ..models import User
class LoginForm(FlaskForm):
    email = StringField('邮箱:',validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField('密码：',validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistretionForm(FlaskForm):
    email = StringField('邮箱：',validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('用户名：',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9]*$',0,'用户名必须是字母或者数字组成')])
    password = PasswordField('密码：',validators=[DataRequired(),EqualTo('password2',message="密码必须一样.")])
    password2 = PasswordField('确认密码：',validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册过了.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被注册了.')
