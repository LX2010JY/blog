from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo

#定义表单
class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')
class EditProfileForm(FlaskForm):
    name = StringField('真实姓名',validators=[Length(0,64)])
    location = StringField('家庭地址',validators=[Length(0,64)])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('确认')


class PostForm(FlaskForm):
    body = TextAreaField("what's your mind?",validators=[DataRequired()])
    submit = SubmitField('发布')
