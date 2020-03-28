from flask import Flask, request, render_template, url_for
import sys
sys.path.insert(1, './db')
from db import new_db_instance

db = new_db_instance()
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
  return render_template("homepage.html")

@app.route('/log_in', methods=['GET'])
def log_in():
  return render_template("log_in.html")

@app.route('/log_in_attempt', methods=['POST'])
def log_in_attempt():
  username = request.form['username']
  password = request.form['password']
  is_valid = db.valid_account(username, password)
  if is_valid[0] == False:
    return render_template("log_in.html", is_valid=is_valid[0], error = is_valid[1])

  return render_template("success.html", is_valid=is_valid[0], error=is_valid[1])

@app.route('/register', methods=['POST', 'GET'])
def register():
  return render_template("register.html")

@app.route('/account_creation', methods=['POST'])
def account_creation():
  account_details = {'first_name' : 'null', 'middle_name' : 'null', 'last_name' : 'null', 'user_name' : 'null', 'password' : 'null', 
                    'street_number' : 'null', 'street_name' : 'null', 'apt_number' : 'null', 'postal_code' : 'null', 'date_of_birth' : 'null',
                    'country' : 'null', 'province' : 'null'}

  #inputs that can't be "null"
  required_inputs = ['first_name', 'last_name', 'username', 'password', 'country', 'street_number', 'street_name', 
                    'province', 'postal_code', 'date_of_birth']
  try:
    account_details['first_name'] = request.form['first_name']
    account_details['middle_name'] = request.form['middle_name']
    account_details['last_name'] = request.form['last_name']
    account_details['username'] = request.form['username']
    account_details['password'] = request.form['password']
    account_details['street_number'] = request.form['street_number']
    account_details['street_name'] = request.form['street_name']
    account_details['apt_number'] = request.form['apt_number']
    account_details['postal_code'] = request.form['postal_code']
    account_details['date_of_birth'] = request.form['date_of_birth']
    account_details['country'] = request.form['country']
    account_details['province'] = request.form['province']
  
  except KeyError as e:
    return "Please enter your country/province"

  error_string = ''
  for required_input in required_inputs:
    if account_details[required_input] == 'null':
      error_string += required_input + ", "
  
  if len(error_string) > 0:
    error_string += "cannot be empty!"
    return error_string
  
  else:
    success = db.create_user(account_details)
    

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