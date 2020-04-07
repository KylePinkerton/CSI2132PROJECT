from flask import Flask, request, render_template, url_for, flash, redirect, abort
import sys
from PIL import Image
sys.path.insert(1, './db')
from db import db
from forms import RegistrationForm, LoginForm, AccountPicture, ChangeNumber, GetVerified, UpdateAbout, UpdateLanguages, UpdateWork, CreateProperty, PaymentMethod, PayoutMethod, AvailableDates, SearchProperty, Admin, AssignEmployeeToProperty
from flask_login import LoginManager, login_required, current_user, logout_user 
from flask_login import UserMixin, login_user
import secrets
import os
import datetime

app = Flask(__name__)
@app.context_processor
def inject_stats():
  db.get_total_users()
  total_users = db.fetch_one()[0]
  db.get_total_properties()
  total_properties = db.fetch_one()[0]
  db.get_total_completed_stays()
  total_completed_stays = db.fetch_one()[0]
  db.get_total_countrys()
  total_countrys = db.fetch_one()[0]
  return dict(total_users=total_users, total_properties=total_properties, total_completed_stays=total_completed_stays, total_countrys=total_countrys)

#app.debug = True
app.config['SECRET_KEY'] = 'f7db6a2ebd1d01417597c005cb404b63'
login_manager = LoginManager(app)
login_manager.login_view = 'log_in'
login_manager.login_message_category = 'info'

class User(UserMixin):
  pass

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

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
    #check if admin
    db.check_admin(username)
    admin_count = db.fetch_one() 
    if admin_count[0]:
      user.admin = True
    else:
      user.admin = False
    #check employee
    db.check_employee(username)
    employee_count = db.fetch_one()
    if employee_count[0]:
      user.employee = True
      #check what kind of employee
      db.get_title(username)
      user.title = db.fetch_one()[0]
      #get manager
      db.get_manager(username)
      user.manager = db.fetch_one()[0]
    else:
      user.employee = False
    return user
  return

@app.route('/')
def index():
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername', 'picture']
  properties = []
  db.get_homepage_properties()
  property_rows = db.fetch_all()

  for row in property_rows:
    property_map = {}
    for k in range(len(property_columns)):
      property_map[property_columns[k]] = row[k]
    
    properties.append(property_map)
  
  for prop in properties:
    db.get_picture(prop['hostusername'])
    picture = db.fetch_one()[0]
    prop['profile_picture'] = picture
  
  return render_template("homepage.html", properties=properties)


@app.route('/search', methods=['GET', 'POST'])
def search():
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername', 'picture']
  form = SearchProperty()
  property_details = {}

  if form.validate_on_submit():
    try: 
      property_details['hostusername'] = request.form.get('hostusername', default='null')
      property_details['propertyname'] = request.form.get('propertyname', default='null')
      property_details['rent_rate'] = request.form.get('rent_rate', default='-1')
      property_details['country'] = request.form.get('country', default='null')
      property_details['province'] = request.form.get('province', default='null')
      property_details['property_type'] = request.form.get('property_type', default='null').lower()
      property_details['max_guests'] = request.form.get('max_guests', default='-1')
      property_details['number_beds'] = request.form.get('number_beds', default='-1')
      property_details['number_baths'] = request.form.get('number_baths', default='-1')
      property_details['accessible'] = request.form.get('accessible', default='null')
      property_details['pets_allowed'] = request.form.get('pets_allowed', default='null')
      #deal with weird cases for optional (can be null) arguments
      for key in property_details:
        if property_details[key] in ['null', '-1', 'None', ""]:
          property_details[key] = key
        else:
          property_details[key] = "'" + str(property_details[key]) + "'"

      properties = []
      db.get_search_properties(property_details['hostusername'], property_details['propertyname'], property_details['rent_rate'], property_details['country'], property_details['province'], property_details['property_type'], property_details['max_guests'], property_details['number_beds'], property_details['number_baths'], property_details['accessible'], property_details['pets_allowed'])
      property_rows = db.fetch_all()
      for row in property_rows:
        property_map = {}
        for k in range(len(property_columns)):
          property_map[property_columns[k]] = row[k]
        properties.append(property_map)

      for prop in properties:
        db.get_picture(prop['hostusername'])
        picture = db.fetch_one()[0]
        prop['profile_picture'] = picture
      
      flash('Successful search. Here are your results:', 'success')
      return render_template("search_results.html", properties=properties)

    except Exception as e:
      db.close()
      db.new_connection()
      print(e)
      flash('Opps, something went wrong. Try again.', 'danger')

  return render_template("search.html", form=form)

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
      db.valid_country(account_details['country'])
      country_count = db.fetch_one()
      if not country_count[0]:
        raise Exception('Sorry, we are not operating in that country yet!')
      if account_details['middle_name'] == "":
        account_details['middle_name'] = "NULL"
      if account_details['apt_number'] == "":
        account_details['apt_number'] = "NaN"
      if account_details['country'] == "-1" or len(account_details['province']) == 0:
        raise Exception('Please enter a country or province')
      db.create_user(account_details['first_name'], account_details['middle_name'], account_details['last_name'], account_details['username'], account_details['password'], account_details['street_number'], account_details['street_name'], account_details['apt_number'], account_details['postal_code'], account_details['date_of_birth'], account_details['country'], account_details['province'], account_details['email'], account_details['phone_number'])
      flash(f'Account created for {form.username.data}!', 'success')
      db.commit()
      return redirect(url_for('index'))
  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    flash('Error: ' + str(e), 'danger')
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

def save_property_picture(form_picture):
  random_name = secrets.token_hex(6)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_name + f_ext
  picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

  output_size = (750, 500)
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
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername', 'picture']
  properties = []
  db.get_users_properties(current_user.id)
  property_rows = db.fetch_all()

  if property_rows == None:
    abort(404)
    return

  for row in property_rows:
    property_map = {}
    for k in range(len(property_columns)):
      property_map[property_columns[k]] = row[k]
    
    properties.append(property_map)

  current_user.properties = properties
  return render_template('your_properties.html')

@app.route("/paymentmethod", methods=["GET", "POST"])
@login_required
def your_payment_method():
  methods_columns = ['username', 'card_type', 'first_name', 'last_name', 'card_number', 'card_expiration', 'cvv', 'billing_country']
  methods = []
  db.get_users_payment_methods(current_user.id)
  methods_rows = db.fetch_all()

  if methods_rows == None:
    abort(404)
    return

  for row in methods_rows:
    methods_map = {}
    for k in range(len(methods_columns)):
      methods_map[methods_columns[k]] = row[k]
    
    methods.append(methods_map)

  current_user.methods = methods
  return render_template('your_payment_method.html', methods=methods)

@app.route("/addproperty", methods=["GET", "POST"])
@login_required
def add_property():
  property_details = {}
  form = CreateProperty()
  try:
    if form.validate_on_submit():
      property_details['hostusername'] = current_user.id
      property_details['property_name'] = request.form.get('property_name')
      property_details['street_number'] = request.form.get('street_number', default='NULL')
      property_details['street_name'] = request.form.get('street_name')
      property_details['apt_number'] = request.form.get('apt_number')
      property_details['postal_code'] = request.form.get('postal_code')
      property_details['rent_rate'] = request.form.get('rent_rate')
      property_details['country'] = request.form.get('country')
      property_details['province'] = request.form.get('province')
      property_details['property_type'] = request.form.get('property_type').lower()
      property_details['max_guests'] = request.form.get('max_guests')
      property_details['number_beds'] = request.form.get('number_beds')
      property_details['number_baths'] = request.form.get('number_baths')
      property_details['accessible'] = request.form.get('accessible')
      property_details['pets_allowed'] = request.form.get('pets_allowed')
      property_details['picture'] = request.form.get('picture')
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
      
      if property_details['country'] == "-1" or len(property_details['province']) == 0:
        raise Exception('Please enter a country or province')
      
      picture_file = save_property_picture(form.picture.data)
      db.create_property(property_details['property_name'], property_details['street_number'], property_details['street_name'], property_details['apt_number'], property_details['postal_code'], property_details['rent_rate'], property_details['country'], property_details['province'], property_details['property_type'], property_details['max_guests'], property_details['number_beds'], property_details['number_baths'], property_details['accessible'], property_details['pets_allowed'], property_details['hostusername'], picture_file)
      flash(f'Property created for {form.property_name.data}!', 'success')
      db.commit()
      return redirect(url_for('your_properties'))
  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    flash('Please enter your country/province', 'danger')
    return render_template('add_property.html', title='Add Property', form=form)
  return render_template('add_property.html', title='Add Property', form=form)

@app.route("/property/<string:propertyname>", methods=['GET', 'POST'])
def individual_property(propertyname):
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername', 'picture']
  db.get_property(propertyname)
  property_rows = db.fetch_one()
  if property_rows == None:
    abort(404)
    return
  property_map = {}
  for i, column in enumerate(property_rows, 0):
    property_map[property_columns[i]] = column

  host_username = property_map['hostusername']
  db.get_picture(host_username)
  host_picture = db.fetch_one()[0]
  form = AvailableDates()
  if request.method == 'POST':
    try:
      available_dates = {}
      available_dates['start_date'] = request.form.get('start_date')
      available_dates['end_date'] = request.form.get('end_date')
      if available_dates['start_date'] in [None, ""]:
        raise Exception("Please choose a Start Date")
      if available_dates['end_date'] in [None, ""]:
        raise Exception("Please choose an End Date")

      start_month, start_day, start_year = [int(x) for x in str(available_dates['start_date']).split('/')] 
      end_month, end_day, end_year = [int(x) for x in str(available_dates['end_date']).split('/')] 
      start_date = datetime.date(start_year, start_month, start_day)
      end_date = datetime.date(end_year, end_month, end_day)

      if start_date > end_date:
        raise Exception("Start date cannot be greater than end date!")

      date_difference = end_date - start_date
      if date_difference.days > 13: 
        raise Exception("You can only stay at one property for a maximum of 14 days!")

      delta = datetime.timedelta(days=1)
      dates = []

      while start_date <= end_date:
        dates.append(start_date)
        start_date += delta
      
      taken_dates = db.check_dates(property_map['propertyname'], dates)

      if len(taken_dates) == 0:
        flash('The property is available during those dates!', 'success')

      else:
        error_message = ""
        for date in taken_dates:
          error_message += date.strftime('%Y-%m-%d') + ", "
        flash('Sorry, the property is not available on the following dates: ' + error_message , 'danger')

    except Exception as e: 
      db.close()
      db.new_connection()
      flash('Error: ' + str(e), 'danger')

  return render_template('property.html', property_map = property_map, host_picture=host_picture, form=form)

@app.route("/<string:username>")
def user_profile(username):
  user_columns = ['username', 'join_date', 'verified', 'about', 'languages', 'work', 'profile_picture']
  db.get_user(username)
  user_rows = db.fetch_one()
  if user_rows == None:
    abort(404)
    return

  user_map = {}
  for i, column in enumerate(user_rows, 0):
    user_map[user_columns[i]] = column
  return render_template('user_profile.html', user_map = user_map)

@app.route("/<string:username>/properties")
def user_properties(username):
  property_columns = ['propertyname', 'street_number', 'street_name', 'apt_number', 'province', 'postal_code', 'rent_rate', 'type', 'max_guests', 'number_beds', 'number_baths', 'accesible', 'pets_allowed', 'country', 'hostusername', 'picture']
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
    db.close()
    return "Server shutting down..."

@app.route("/addpaymentmethod", methods=["GET", "POST"])
@login_required
def add_payment_method():
  payment_method = {}
  form = PaymentMethod()
  try: 
    if form.validate_on_submit():
      payment_method['username'] = current_user.id
      payment_method['card_type'] = request.form.get('card_type').lower()
      payment_method['first_name'] = request.form.get('first_name')
      payment_method['last_name'] = request.form.get('last_name')
      payment_method['card_number'] = request.form.get('card_number')
      payment_method['card_expiration'] = request.form.get('card_expiration')
      payment_method['cvv'] = str(request.form.get('cvv'))
      payment_method['billing_country'] = request.form.get('billing_country')
      #there's a hidden 'province' field here cuz of country.js btw
      if payment_method['billing_country'] in ["-1", None]:
        raise Exception('Please enter a country or province')

      db.create_payment_method(payment_method['username'], payment_method['card_type'], payment_method['first_name'], payment_method['last_name'], 
        payment_method['card_number'], payment_method['card_expiration'], payment_method['cvv'], payment_method['billing_country'])

      flash(f'Payment method created!', 'success')
      db.commit()
      return redirect(url_for('your_payment_method'))
  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    flash('Please enter your billing country', 'danger')
    return render_template('add_payment_method.html', title='Add Payment Method', form=form)
  return render_template('add_payment_method.html', title='Add Payment Method', form=form)

@app.route("/payoutmethod", methods=["GET", "POST"])
@login_required
def your_payout_method():
  methods_columns = ['username', 'paypal_address']
  methods = []
  db.get_users_payout_methods(current_user.id)
  methods_rows = db.fetch_all()

  if methods_rows == None:
    abort(404)
    return

  for row in methods_rows:
    methods_map = {}
    for k in range(len(methods_columns)):
      methods_map[methods_columns[k]] = row[k]
    
    methods.append(methods_map)

  current_user.methods = methods
  return render_template('your_payout_method.html', methods=methods)

@app.route("/addpayoutmethod", methods=["GET", "POST"])
@login_required
def add_payout_method():
  payout_method = {}
  form = PayoutMethod()
  if form.validate_on_submit():
    payout_method['username'] = current_user.id
    payout_method['paypal_address'] = request.form.get('paypal_address')
    db.create_payout_method(payout_method['username'], payout_method['paypal_address'])
    flash(f'Payout method created!', 'success')
    db.commit()
    return redirect(url_for('your_payout_method'))
  return render_template('add_payout_method.html', title='Add Payout Method', form=form)

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
  if current_user.admin == True:
    form = Admin()
    try: 
      if form.validate_on_submit():
        query = request.form.get('query')
        db.raw_query(query)
        result = None
        try:
          result = db.fetch_all()
        except Exception as e:
          print(e)
        if result == None: 
          flash(f'Successful query. Your query was: ' + query, 'success')
          db.commit()
          return render_template('admin.html', form=form, result=[])
        else:
          flash(f'Successful query. Your query was: ' + query, 'success')
          db.commit()
          return render_template('admin.html', form=form, result=result)

    except Exception as e:
      flash('The following error ocurred when executing your query: ' + str(e), 'danger')
      db.close()
      db.new_connection()
      return render_template('admin.html', form=form, result=[])
    return render_template('admin.html', form=form, result=[])
  else:
    abort(404)

@app.route("/assignedproperties", methods=["GET", "POST"])
@login_required
def assigned_properties():
  if (current_user.title != "Admin" and current_user.title != "Master Admin" and current_user.title != "Branch Manager"):
    assigned_properties = []
    db.get_assigned_properties(current_user.id)
    properties = db.fetch_all()
    for assigned_property in properties:
      property_map = {}
      property_map['propertyname'] = assigned_property[0]
      property_map['street_name'] = assigned_property[1]
      property_map['street_number'] = assigned_property[2]
      property_map['postal_code'] = assigned_property[3]
      property_map['province'] = assigned_property[4]
      property_map['country'] = assigned_property[5]
      assigned_properties.append(property_map)
    return render_template('assignedproperties.html', assigned_properties=assigned_properties)
  else:
    abort(404)

@app.route("/branchmanagerportal", methods=["GET", "POST"])
@login_required
def branchmanagerportal():
  if (current_user.title == "Branch Manager"):
    return render_template('branchmanagerportal.html')
  else:
    abort(404)

@app.route("/viewemployees", methods=["GET", "POST"])
@login_required
def view_employees():
  if (current_user.title == "Branch Manager"):
    db.view_employees(current_user.country)
    employees_query = db.fetch_all()
    employees = []
    for employee in employees_query:
      employee_map = {}
      employee_map['assigned_properties']= []
      employee_map['username'] = employee[0]
      employee_map['title'] = employee[1]
      employee_map['salary'] = employee[2]
      employee_map['country'] = employee[3]
      employee_map['managerusername'] = employee[4]

      db.get_assigned_properties(employee[0])
      properties = db.fetch_all()
      for assigned_property in properties:
        property_map = {}
        property_map['propertyname'] = assigned_property[0]
        property_map['street_name'] = assigned_property[1]
        property_map['street_number'] = assigned_property[2]
        property_map['postal_code'] = assigned_property[3]
        property_map['province'] = assigned_property[4]
        property_map['country'] = assigned_property[5]
        employee_map['assigned_properties'].append(property_map)
      employees.append(employee_map)    
    
    return render_template('view_employees.html', employees = employees)
  else:
    abort(404)

@app.route("/shorttermavailableproperties", methods=["GET", "POST"])
@login_required
def short_term_available_properties():
  if (current_user.title == "Branch Manager"):
    assigned_properties = []
    db.get_short_term_available_properties(current_user.country)
    properties = db.fetch_all()
    available_properties = []
    for available_property in properties:
      property_map = {}
      property_map['propertyname'] = available_property[0]
      property_map['street_number'] = available_property[1]
      property_map['street_name'] = available_property[2]
      property_map['apt_number'] = available_property[3]
      property_map['province'] = available_property[4]
      property_map['postal_code'] = available_property[5]
      property_map['country'] = available_property[13]
      available_properties.append(property_map)
    return render_template('short_term_available.html', available_properties=available_properties)

  else:
    abort(404)

@app.route("/shorttermunavailableproperties", methods=["GET", "POST"])
@login_required
def short_term_unavailable_properties():
  if (current_user.title == "Branch Manager"):
    assigned_properties = []
    db.get_short_term_unavailable_properties(current_user.country)
    properties = db.fetch_all()
    unavailable_properties = []
    for unavailable_property in properties:
      property_map = {}
      property_map['propertyname'] = unavailable_property[0]
      property_map['street_number'] = unavailable_property[1]
      property_map['street_name'] = unavailable_property[2]
      property_map['apt_number'] = unavailable_property[3]
      property_map['province'] = unavailable_property[4]
      property_map['postal_code'] = unavailable_property[5]
      property_map['country'] = unavailable_property[13]
      unavailable_properties.append(property_map)
    return render_template('short_term_unavailable.html', unavailable_properties=unavailable_properties)

  else:
    abort(404)

@app.route("/assignemployee", methods=["GET", "POST"])
@login_required
def assign_employee_to_property():
  try:
    if (current_user.title == "Branch Manager"):
      assign_map = {}
      form = AssignEmployeeToProperty()
      if form.validate_on_submit():
        assign_map['employeeusername'] = request.form.get('employeeusername')
        assign_map['propertyname'] = request.form.get('propertyname')
        #ensure employee and property are from this branch manager's branch (country)
        db.get_property_country(assign_map['propertyname'])
        property_country = db.fetch_one()
        db.get_employee_country(assign_map['employeeusername'])
        employee_country = db.fetch_one()

        if employee_country == None:
          raise Exception("This user is not an employee!")
        
        if property_country == None:
          raise Exception("This property is not part of your branch")

        property_country = property_country[0]
        employee_country = employee_country[0]

        if (current_user.country != property_country):
          raise Exception("This property is not part of your branch!")
        
        if (current_user.country != employee_country):
          raise Exception("This employee is not part of your branch!")
        
        db.assign_employee_to_property(assign_map['employeeusername'], assign_map['propertyname'])
        db.commit()

        flash('Success! ' + assign_map['employeeusername'] + ' has been assigned to the property ' + assign_map['propertyname'], 'success')
        return render_template('assign_employee_to_property.html', form=form)

    else:
      abort(404)

  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    flash('Error: ' + str(e), 'danger')
    return render_template('assign_employee_to_property.html', form=form)
  
  return render_template('assign_employee_to_property.html', form=form)
    
    
if __name__ == "__main__":
  app.run()