from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Regexp, ValidationError
from db import db
import phonenumbers

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
  street_name = StringField('Street Name', validators=[DataRequired(), Length(min=1, max=20)])
  apt_number = StringField('Apartment Number (optional)', validators=[Length(max=5)])
  postal_code = StringField('Postal Code',
                          validators=[DataRequired(), Length(min=6, max=20)])
  date_of_birth = DateField('Date of Birth (yyyy-mm-dd)',
                          validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
  phone_number = StringField('Phone', validators=[DataRequired()])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    db.valid_username(username.data)
    username_count = db.fetch_one()
    if username_count[0]:
      raise ValidationError("That username is taken. Please choose another username.")
  
  def validate_phone(form, field):
    if len(field.data) > 16:
      raise ValidationError('Invalid phone number.')
    try:
      input_number = phonenumbers.parse(field.data)
      if not (phonenumbers.is_valid_number(input_number)):
        raise ValidationError('Invalid phone number.')
    except:
      input_number = phonenumbers.parse("+1"+field.data)
      if not (phonenumbers.is_valid_number(input_number)):
        raise ValidationError('Invalid phone number.')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Log In')

class AccountPicture(FlaskForm):
  picture = FileField('Update Profile Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Update')