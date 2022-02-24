import wtforms
from wtforms.validators import length, email,EqualTo
from wtforms.validators import DataRequired


class LoginForm(wtforms.Form):
    email = wtforms.StringField('Email', validators=[DataRequired
            (message=u"Email cannot be empty"), length(min=5, max=20), email()])
    password = wtforms.StringField('Password', validators=[DataRequired
            (message=u'Password cannot be empty'), length(min=6, max=20)])


class SignupForm(wtforms.Form):
    name = wtforms.StringField('Name', validators=[DataRequired
            (message=u'name cannot be empty'), length(min=1, max=8)])
    age = wtforms.IntegerField('Age', validators=[DataRequired
            (message=u'age cannot be empty')])
    email = wtforms.StringField('Email', validators=[DataRequired
            (message=u'Email cannot be empty'), length(min=5, max=20), email()])
    password = wtforms.StringField('Password', validators=[DataRequired
            (message=u'Password cannot be empty'), length(min=6, max=20)])
    pw_confirm = wtforms.StringField('Confirm Password', validators=[EqualTo("password")])


