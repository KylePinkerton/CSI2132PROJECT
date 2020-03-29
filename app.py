from flask import Flask, request, render_template, url_for, flash, redirect
import sys
sys.path.insert(1, './db')
from db import db
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_required, current_user, logout_user
from flask_login import UserMixin, login_user

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
  account_details = {'first_name' : 'NULL', 'middle_name' : 'NULL', 'last_name' : 'NULL', 'user_name' : 'NULL', 'password' : 'NULL', 
                    'street_number' : 'NULL', 'street_name' : 'NULL', 'apt_number' : 'NULL', 'postal_code' : 'NULL', 'date_of_birth' : 'NULL',
                    'country' : 'NULL', 'province' : 'NULL'}

  form = RegistrationForm()
  try:
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
      #deal with weird cases for optional (can be null) arguments
      if account_details['middle_name'] == "":
        account_details['middle_name'] = "NULL"
      if account_details['apt_number'] == "":
        account_details['apt_number'] = "NaN"
      db.create_user(account_details['first_name'], account_details['middle_name'], account_details['last_name'], account_details['username'], account_details['password'], account_details['street_number'], account_details['street_name'], account_details['apt_number'], account_details['postal_code'], account_details['date_of_birth'], account_details['country'], account_details['province'])
      flash(f'Account created for {form.username.data}!', 'success')
      db.commit()
      return redirect(url_for('index'))
  except Exception as e:
    print(e)
    flash('Please enter your country/province', 'danger')
    return render_template('register.html', title='Register', form=form)
  return render_template('register.html', title='Register', form=form)

@app.route("/account")
@login_required
def account():
  return render_template('account.html', title='Account')

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