from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, length,EqualTo


class LoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired
            (message=u"Email cannot be empty"), length(min=5, max=50)])
        password = StringField('Password', validators=[DataRequired
            (message=u'Password cannot be empty'), length(min=1, max=50)])


class SignupForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired
            (message=u'Username cannot be empty'), length(min=1, max=8)])
        age = IntegerField('Age', validators=[DataRequired
            (message=u'Age cannot be empty')])
        email = StringField('Email', validators=[DataRequired
            (message=u'Email cannot be empty'), length(min=5, max=50)])
        password = StringField('Password', validators=[DataRequired
            (message=u'Password cannot be empty'), length(min=1, max=50)])
        pw_confirm = StringField('Confirm Password')

class BookingForm(FlaskForm):
        duration = IntegerField('Duration', validators=[DataRequired
            (message=u'Duration is required')])
        location = StringField('Location', validators=[DataRequired
            (message=u'Location is required')])


class ScooterForm(FlaskForm):
        available = IntegerField('Available', validators=[DataRequired
            (message=u'Available is required')])
        location = StringField('Location', validators=[DataRequired
            (message=u'Location is required')])

class PriceForm(FlaskForm):

        cost = IntegerField('Cost', validators=[DataRequired
            (message=u'Cost is required')])

class AddPriceForm(FlaskForm):
        duration = IntegerField('Duration', validators=[DataRequired
            (message=u'Duration is required')])
        cost = IntegerField('Cost', validators=[DataRequired
            (message=u'Cost is required')])


class CardForm(FlaskForm):
        number = StringField('number', validators=[DataRequired
                                             (message=u"Card Number required")])
        expiration_date = StringField('expiration_date', validators=[DataRequired
                                                   (message=u"Expiration date required")])
        security_code = IntegerField('security_code', validators=[DataRequired
                                                   (message=u"CVV / CVC required")])
        name = StringField('name', validators=[DataRequired
                                                   (message=u"Name on Card required")])
        save = BooleanField('security_code')
