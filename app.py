from flask import Flask, request, render_template, url_for, flash, redirect
import sys
sys.path.insert(1, './db')
from db import new_db_instance
from forms import RegistrationForm, LoginForm

db = new_db_instance()
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'f7db6a2ebd1d01417597c005cb404b63'

@app.route('/')
def index():
  return render_template("homepage.html")

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
  form = LoginForm()
  if form.validate_on_submit():
      if form.username.data == 'admin' and form.password.data == 'admin':
          flash('You have been logged in!', 'success')
          return redirect(url_for('index'))
      else:
          flash('Login Unsuccessful. Please check username and password', 'danger')
  return render_template('log_in.html', title='Login', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
  form = RegistrationForm()
  try:
    if form.validate_on_submit():
      country = request.form['country']
      province = request.form['province']
      flash(f'Account created for {form.username.data}!', 'success')
      return redirect(url_for('index'))

  except Exception as e:
    print(e)
    flash('Please enter your country/province', 'danger')
    return render_template('register.html', title='Register', form=form)
  return render_template('register.html', title='Register', form=form)


@app.route('/account_creation', methods=['POST'])
def account_creation():
  pass
    

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