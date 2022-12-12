# flask forms, using wtforms
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from database import DatabaseAPI


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        database = DatabaseAPI()
        user = database.verify_email(field.data)
        if user is not None:
            raise ValidationError('Email already registered.')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New password', validators=[
                                 DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm new password')
    submit = SubmitField('Change password')


class PaymentForm(FlaskForm):
    tier = StringField('Tier', validators=[DataRequired()])
    submit = SubmitField('Pay')
