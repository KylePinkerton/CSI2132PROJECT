from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Regexp


class RegistrationForm(FlaskForm):
  first_name = StringField('First Name',
                          validators=[DataRequired(), Length(min=1, max=20)])
  middle_name = StringField('Middle Name (optional)',
                          validators=[Length(max=20)])
  last_name = StringField('Last Name',
                          validators=[DataRequired(), Length(min=1, max=20)])
  username = StringField('Username',
                          validators=[DataRequired(), Length(min=1, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
  street_number = IntegerField('Street Number', validators=[DataRequired(), NumberRange(min=1, max=99999)])
  apt_number = StringField('Apartment Number (optional)', validators=[Length(max=5)])
  postal_code = StringField('Postal Code',
                          validators=[DataRequired(), Length(min=6, max=20)])
  date_of_birth = DateField('Date of Birth (yyyy-mm-dd)',
                          validators=[DataRequired()])
  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')