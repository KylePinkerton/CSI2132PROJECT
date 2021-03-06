from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Regexp, ValidationError, Optional
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
    if " " in list(username.data):
      raise ValidationError("No whitespace in usernames.")

  
  def validate_phone_number(form, phone_number):
    if len(phone_number.data) > 16:
      raise ValidationError('Invalid phone number.')
    try:
      input_number = phonenumbers.parse(phone_number.data)
      if not (phonenumbers.is_valid_number(input_number)):
        raise ValidationError('Invalid phone number.')
    except Exception as e:
      try:
        input_number = phonenumbers.parse("+1"+phone_number.data)
        if not (phonenumbers.is_valid_number(input_number)):
          raise ValidationError('Invalid phone number.')
      except Exception as e:
        raise ValidationError('Invalid phone number.')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Log In')

class AccountPicture(FlaskForm):
  picture = FileField('Update Profile Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Update')

class ChangeNumber(FlaskForm):
  phone_number = StringField('Phone', validators=[DataRequired()])
  submit = SubmitField('Update')

  def validate_phone_number(form, phone_number):
    if len(phone_number.data) > 16:
      raise ValidationError('Invalid phone number.')
    try:
      input_number = phonenumbers.parse(phone_number.data)
      if not (phonenumbers.is_valid_number(input_number)):
        raise ValidationError('Invalid phone number.')
    except Exception as e:
      try:
        input_number = phonenumbers.parse("+1"+phone_number.data)
        if not (phonenumbers.is_valid_number(input_number)):
          raise ValidationError('Invalid phone number.')
      except Exception as e:
        raise ValidationError('Invalid phone number.')

class GetVerified(FlaskForm):
  verified = BooleanField('Would you like to be verified?', validators=[DataRequired()])
  submit = SubmitField('Get Verified')

class UpdateAbout(FlaskForm):
  about = StringField('About',
                          validators=[DataRequired(), Length(min=1, max=100)])
  submit = SubmitField('Update')

class UpdateLanguages(FlaskForm):
  languages = StringField('Languages',
                          validators=[DataRequired(), Length(min=1, max=50)])
  submit = SubmitField('Update')

class UpdateWork(FlaskForm):
  work = StringField('Work',
                          validators=[DataRequired(), Length(min=1, max=50)])
  submit = SubmitField('Update')

class CreateProperty(FlaskForm):
  property_name = StringField('Property Name',
                          validators=[DataRequired(), Length(min=1, max=20)])
  street_number = IntegerField('Street Number', validators=[DataRequired(), NumberRange(min=1, max=99999)])
  street_name = StringField('Street Name', validators=[DataRequired(), Length(min=1, max=20)])
  apt_number = StringField('Apartment Number (optional)', validators=[Length(max=5)])
  postal_code = StringField('Postal Code',
                          validators=[DataRequired(), Length(min=6, max=20)])
  rent_rate = IntegerField('Rent Rate (Per Night)',
                          validators=[DataRequired(), NumberRange(min=1, max=9999)])
  property_type = StringField('Property Type (Entire, Private, or Shared)', validators=[DataRequired()])
  max_guests = IntegerField('Maximum Guests',
                          validators=[DataRequired(), NumberRange(min=1, max=99)])
  number_beds = IntegerField('Number of Beds',
                          validators=[DataRequired(), NumberRange(min=1, max=99)])
  number_baths = IntegerField('Number of Baths',
                          validators=[DataRequired(), NumberRange(min=1, max=99)])  
  accessible = BooleanField('Accessible?')
  pets_allowed = BooleanField('Pets Allowed?')
  picture = FileField('Property Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])                                              
  submit = SubmitField('Create Property')

  def validate_property_name(self, property_name):
    db.valid_propertyname(property_name.data)
    propertyname_count = db.fetch_one()
    if propertyname_count[0]:
      raise ValidationError("That property name is taken. Please choose another propertyname.")
    if " " in list(property_name.data):
      raise ValidationError("No whitespace in property names.")

  def validate_property_type(form, property_type):
    if property_type.data.lower() not in ['entire', 'private', 'shared']:
      raise ValidationError('Invalid property type.')

class PaymentMethod(FlaskForm):
  card_type = StringField('Card Type (Visa or Mastercard required)',
                          validators=[DataRequired(), Length(min=2, max=20)])
  first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=20)])
  last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=20)])
  card_number= StringField('Card Number',
                          validators=[DataRequired(), Length(min=6, max=20)])
  card_expiration = DateField('Date of Birth (yyyy-mm-dd)',
                          validators=[DataRequired()])
  cvv = IntegerField('cvv',
                          validators=[DataRequired(), NumberRange(min=100, max=999)])
  submit = SubmitField('Add Payment Method')

  def validate_card_type(form, card_type):
    if card_type.data.lower() not in ['visa', 'mastercard', 'shared']:
      raise ValidationError('Invalid credit card type.')

class PayoutMethod(FlaskForm):
  paypal_address = StringField('Paypal Address', validators=[DataRequired(), Email(), Length(min=7, max=40)])
  submit = SubmitField('Add Payout Method')
 

class AvailableDates(FlaskForm):
  #dummy field to let us use wtforms with js calender
  dummy = DateField('Dummy')
  submit = SubmitField('Check Availability')

class SearchProperty(FlaskForm):
  propertyname = StringField('Property Name', validators=[Optional()])
  hostusername = StringField('Host Username', validators=[Optional()])
  rent_rate = IntegerField('Maximum Rent Rate ($ Per Night)', validators=[Optional()])
  property_type = StringField('Property Type (Entire, Private, or Shared)', validators=[Optional()])
  max_guests = IntegerField('Minimum Guests Allowed', validators=[Optional()])
  number_beds = IntegerField('Minimum Number of Beds', validators=[Optional()])
  number_baths = IntegerField('Minimum Number of Baths', validators=[Optional()])
  accessible = BooleanField('Accessible?', validators=[Optional()])
  pets_allowed = BooleanField('Pets Allowed?', validators=[Optional()])
  submit = SubmitField('Search for property!')

class Admin(FlaskForm):
  query = TextAreaField('Enter Your Query: ', validators=[DataRequired()])
  submit = SubmitField('Perform query')

class AssignEmployeeToProperty(FlaskForm):
  employeeusername = StringField('Employee Username', validators=[DataRequired()])
  propertyname = StringField('Property Name', validators=[DataRequired()])
  submit = SubmitField('Assign Employee to Property')

  def validate_branch_propertyname(self, propertyname):
    db.valid_propertyname(propertyname.data)
    propertyname_count = db.fetch_one()
    if not propertyname_count[0]:
      raise ValidationError("That property does not exist, please choose another.")
    if " " in list(property_name.data):
      raise ValidationError("No whitespace in property names.")
  
  def validate_employeeusername(self, employeeusername):
    db.valid_username(employeeusername.data)
    employeeusername_count = db.fetch_one()
    if not employeeusername_count[0]:
      raise ValidationError("That employeeusername does not exist.")
    if " " in list(employeeusername.data):
      raise ValidationError("No whitespace in employeeusernames.")
