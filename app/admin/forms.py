from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo

