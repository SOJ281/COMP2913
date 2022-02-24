import wtforms
from wtforms.validators import length, email
from wtforms.validators import DataRequired


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[length(min=5,max=20), email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class SignupForm(wtforms.Form):
    name = wtforms.StringField('Name', validators=[DataRequired()])
    age = wtforms.IntegerField('Age', validators=[DataRequired()])
    email = wtforms.StringField('Email', validators=[DataRequired()])
    password = wtforms.StringField('Password', validators=[DataRequired()])


