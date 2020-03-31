from flask import Flask, request, render_template, url_for, flash, redirect
import sys
from PIL import Image
sys.path.insert(1, './db')
from db import db
from forms import RegistrationForm, LoginForm, AccountPicture, ChangeNumber, GetVerified, UpdateAbout, UpdateLanguages, UpdateWork, CreateProperty
from flask_login import LoginManager, login_required, current_user, logout_user
from flask_login import UserMixin, login_user
import secrets
import os

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'f7db6a2ebd1d01417597c005cb404b63'
login_manager = LoginManager(app)
login_manager.login_view = 'log_in'
login_manager.login_message_category = 'info'

class User(UserMixin):
  pass

@login_manager.user_loader
def user_loader(username):
  db.valid_username(username)
  username_count = db.fetch_one()
  user = User()
  if username_count[0]:
    user.id = username
    #do a bunch of initializations????
    #peron table
    db.select_from_person(username, 'first_name')
    user.first_name = db.fetch_one()[0]
    db.select_from_person(username, 'middle_name')
    user.middle_name = db.fetch_one()[0]
    db.select_from_person(username, 'last_name')
    user.last_name = db.fetch_one()[0]
    db.select_from_person(username, 'password')
    user.password = db.fetch_one()[0]
    db.select_from_person(username, 'street_number')
    user.street_number = db.fetch_one()[0]
    db.select_from_person(username, 'street_name')
    user.street_name = db.fetch_one()[0]
    db.select_from_person(username, 'apt_number')
    user.apt_number = db.fetch_one()[0]
    db.select_from_person(username, 'postal_code')
    user.postal_code = db.fetch_one()[0]
    db.select_from_person(username, 'date_of_birth')
    user.date_of_birth = db.fetch_one()[0]
    db.select_from_person(username, 'country')
    user.country = db.fetch_one()[0]
    db.select_from_person(username, 'province')
    user.province = db.fetch_one()[0]
    db.select_from_person_email(username)
    user.email = db.fetch_all()
    db.select_from_person_phone(username)
    user.phone_number = db.fetch_all()
    #users table 
    db.get_join_date(username)
    user.join_date = db.fetch_one()[0]
    db.get_verified(username)
    user.verified = db.fetch_one()[0]
    db.get_about(username)
    user.about = db.fetch_one()[0]
    db.get_languages(username)
    user.languages = db.fetch_one()[0]
    db.get_work(username)
    user.work = db.fetch_one()[0]
    db.get_picture(username)
    user.picture = db.fetch_one()[0]
    return user
  return

@app.route('/')
def index():
  return render_template("homepage.html")

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    db.valid_username(username)
    username_count = db.fetch_one()
    user = User()
    if not username_count[0]:
      flash('Login Unsuccessful. Username does not exist.', 'danger')
      return render_template('log_in.html', title='Login', form=form) 

    db.get_password_from_username(username)
    check_password = db.fetch_one()
    if request.form.get('password') == check_password[0]:
      user.id = username
      login_user(user)
      flash('You have been logged in!', 'success')
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('index'))
    else: 
      flash('Login Unsuccessful. Please check username and password', 'danger')
  return render_template('log_in.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  account_details = {}

  form = RegistrationForm()
  try:
    user = User()
    if form.validate_on_submit():
      account_details['first_name'] = request.form.get('first_name')
      account_details['middle_name'] = request.form.get('middle_name', default='NULL')
      account_details['last_name'] = request.form.get('last_name')
      account_details['username'] = request.form.get('username')
      account_details['password'] = request.form.get('password')
      account_details['street_number'] = request.form.get('street_number')
      account_details['street_name'] = request.form.get('street_name')
      account_details['apt_number'] = request.form.get('apt_number', default='NaN')
      account_details['postal_code'] = request.form.get('postal_code')
      account_details['date_of_birth'] = request.form.get('date_of_birth')
      account_details['country'] = request.form.get('country')
      account_details['province'] = request.form.get('province')
      account_details['email'] = request.form.get('email')
      account_details['phone_number'] = request.form.get('phone_number')
      #deal with weird cases for optional (can be null) arguments
      if account_details['middle_name'] == "":
        account_details['middle_name'] = "NULL"
      if account_details['apt_number'] == "":
        account_details['apt_number'] = "NaN"
      db.create_user(account_details['first_name'], account_details['middle_name'], account_details['last_name'], account_details['username'], account_details['password'], account_details['street_number'], account_details['street_name'], account_details['apt_number'], account_details['postal_code'], account_details['date_of_birth'], account_details['country'], account_details['province'], account_details['email'], account_details['phone_number'])
      flash(f'Account created for {form.username.data}!', 'success')
      db.commit()
      return redirect(url_for('index'))
  except Exception as e:
    print(e)
    flash('Please enter your country/province', 'danger')
    return render_template('register.html', title='Register', form=form)
  return render_template('register.html', title='Register', form=form)

def save_picture(form_picture):
  random_name = secrets.token_hex(6)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_name + f_ext
  picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

  output_size = (125, 125)
  image = Image.open(form_picture)
  image.thumbnail(output_size)
  image.save(picture_path)
  return picture_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
  form = AccountPicture()
  if form.validate_on_submit():
    picture_file = save_picture(form.picture.data)
    current_user.picture = picture_file
    db.update_picture(current_user.id, picture_file)
    db.commit()
    flash('Your account has been updated', 'success')
  picture = url_for('static', filename='images/' + current_user.picture)
  return render_template('account.html', title='Account', form=form, picture=picture)

@app.route("/accountinfo", methods=["GET", "POST"])
@login_required
def account_info():
  return render_template('account_info.html')
  
@app.route("/changenumber", methods=["GET", "POST"])
@login_required
def account_change_number():
  form = ChangeNumber()
  if form.validate_on_submit():
    phone_number = request.form.get('phone_number')
    print(phone_number)
    db.update_phone_number(current_user.id, phone_number)
    db.commit()
    flash('Your Phone number has been updated', 'success')
    return redirect(url_for('account_info'))
  return render_template('account_change_number.html', form=form)

@app.route("/accountgetverified", methods=["GET", "POST"])
@login_required
def account_get_verified():
  form = GetVerified()
  if form.validate_on_submit():
    db.update_verified(current_user.id)
    db.commit()
    flash('Your account has been verified!', 'success')
    return redirect(url_for('account'))
  return render_template('account_get_verified.html', form=form)

@app.route("/accountupdateabout", methods=["GET", "POST"])
@login_required
def account_update_about():
  form = UpdateAbout()
  if form.validate_on_submit():
    about = request.form.get('about')
    db.update_about(current_user.id, about)
    db.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  return render_template('account_update_about.html', form=form)

@app.route("/accountupdatelanguages", methods=["GET", "POST"])
@login_required
def account_update_languages():
  form = UpdateLanguages()
  if form.validate_on_submit():
    languages = request.form.get('languages')
    db.update_languages(current_user.id, languages)
    db.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  return render_template('account_update_languages.html', form=form)

@app.route("/accountupdatework", methods=["GET", "POST"])
@login_required
def account_update_work():
  form = UpdateWork()
  if form.validate_on_submit():
    work = request.form.get('work')
    db.update_work(current_user.id, work)
    db.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('account'))
  return render_template('account_update_work.html', form=form)

@app.route("/yourproperties", methods=["GET", "POST"])
@login_required
def your_properties():
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername']
  properties = []
  db.get_users_properties(current_user.id)
  property_rows = db.fetch_all()

  for row in property_rows:
    property_map = {}
    for k in range(len(property_columns)):
      property_map[property_columns[k]] = row[k]
    
    properties.append(property_map)

  current_user.properties = properties
  return render_template('your_properties.html')

@app.route("/addproperty", methods=["GET", "POST"])
@login_required
def add_property():
  property_details = {}
  form = CreateProperty()
  try:
    if form.validate_on_submit():
      property_details['property_name'] = request.form.get('property_name')
      property_details['street_number'] = request.form.get('street_number', default='NULL')
      property_details['street_name'] = request.form.get('street_name')
      property_details['apt_number'] = request.form.get('apt_number')
      property_details['postal_code'] = request.form.get('postal_code')
      property_details['rent_rate'] = request.form.get('rent_rate')
      property_details['country'] = request.form.get('country')
      property_details['province'] = request.form.get('province')
      property_details['property_type'] = request.form.get('property_type')
      property_details['max_guests'] = request.form.get('max_guests')
      property_details['number_beds'] = request.form.get('number_beds')
      property_details['number_baths'] = request.form.get('number_baths')
      property_details['accessible'] = request.form.get('accessible')
      property_details['pets_allowed'] = request.form.get('pets_allowed')
      #deal with weird cases for optional (can be null) arguments
      if property_details['apt_number'] == "":
        property_details['apt_number'] = "NaN"
      if property_details['postal_code'] == "":
        property_details['postal_code'] = "NULL"
      if property_details['accessible'] == "n":
        property_details['accessible'] = "False"
      else: 
        property_details['accessible'] = "True"
      if property_details['pets_allowed'] == "n":
        property_details['pets_allowed'] = "False"
      else: 
        property_details['pets_allowed'] = "True"
      db.create_property(property_details['property_name'], property_details['street_number'], property_details['street_name'], property_details['apt_number'], property_details['postal_code'], property_details['rent_rate'], property_details['country'], property_details['province'], property_details['property_type'], property_details['max_guests'], property_details['number_beds'], property_details['number_baths'], property_details['accessible'], property_details['pets_allowed'], current_user.id)
      flash(f'Property created for {form.property_name.data}!', 'success')
      db.commit()
      return redirect(url_for('your_properties'))
  except Exception as e:
    print(e)
    flash('Please enter your country/province', 'danger')
    return render_template('add_property.html', title='Add Property', form=form)
  return render_template('add_property.html', title='Add Property', form=form)

@app.route("/property/<string:propertyname>")
def individual_property(propertyname):
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername']
  db.get_property(propertyname)
  property_rows = db.fetch_one()
  property_map = {}
  for i, column in enumerate(property_rows, 0):
    property_map[property_columns[i]] = column

  host_username = property_map['hostusername']
  db.get_picture(host_username)
  host_picture = db.fetch_one()[0]

  return render_template('property.html', property_map = property_map, host_picture=host_picture, host_username=host_username)

@app.route("/<string:username>")
def user_profile(username):
  user_columns = ['username', 'join_date', 'verified', 'about', 'languages', 'work', 'profile_picture']
  db.get_user(username)
  user_rows = db.fetch_one()
  user_map = {}
  for i, column in enumerate(user_rows, 0):
    user_map[user_columns[i]] = column
  return render_template('user_profile.html', user_map = user_map)

@app.route("/<string:username>/properties")
def user_properties(username):
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername']
  properties = []
  db.get_users_properties(username)
  property_rows = db.fetch_all()

  for row in property_rows:
    property_map = {}
    for k in range(len(property_columns)):
      property_map[property_columns[k]] = row[k]
    
    properties.append(property_map)
  
  db.get_picture(username)
  host_picture = db.fetch_one()[0]

  return render_template('user_properties.html', properties=properties, host_picture=host_picture, username=username)


@app.route('/shutdown', methods=['GET'])
def shutdown():
    def shutdown_server():
      func = request.environ.get('werkzeug.server.shutdown')
      if func is None:
          raise RuntimeError('Not running with the Werkzeug Server')
      func()
    shutdown_server()
    db.connection.close()
    return "Server shutting down..."

if __name__ == "__main__":
  app.run()