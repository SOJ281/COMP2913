from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class SignupForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(Form):
    email = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
