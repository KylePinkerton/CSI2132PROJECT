from dbconnection import new_connection
import os
import secrets
from datetime import datetime

class DB:
  def __init__(self, connection):
    self.connection = connection
    self.cursor = self.connection.cursor
  
  def fetch_all(self):
    return self.cursor.fetchall()
  
  def fetch_one(self):
    return self.cursor.fetchone()

  def commit(self):
    self.connection.commit()

  def valid_account(self, username, password):
    try:
      self.cursor.execute(f"select {username} from person")
    
    except Exception as e:
      print(type(e))
      print(e)
      return (False, "Invalid Username")

    try: 
      self.cursor.execute(f"select {username}, {password} from person")

    except Exception as e:
      print(type(e))
      print(e)
      return (False, "Invalid Password")
    
    return (True, "Successful Sign in")

  def valid_username(self, username):
    self.cursor.execute(f"select count(username) from person where username='{username}'")

  def select_from_person(self, username, field):
    self.cursor.execute(f"select {field} from person where username='{username}'")
  
  def select_from_person_email(self, username):
    self.cursor.execute(f"select email_address from person_email_address where username='{username}'")

  def select_from_person_phone(self, username):
    self.cursor.execute(f"select phone_number from person_phone_number where username='{username}'")
  
  def get_picture(self, username):
    self.cursor.execute(f"select profile_picture from users where username='{username}'")
  
  def insert_email(self, username, email):
    self.cursor.execute(f"insert into person_email_address (username, email_address) VALUES ('{username}', '{email}')")
  
  def insert_phone_number(self, username, phone_number):
    self.cursor.execute(f"insert into person_phone_number (username, phone_number) VALUES ('{username}', '{phone_number}')")

  def update_picture(self, username, picture):
    self.cursor.execute(f"update users set profile_picture = '{picture}' WHERE username='{username}'")
  
  def get_password_from_username(self, username):
    self.cursor.execute(f"select password from person where username='{username}'")

  def create_user(self, first_name, middle_name, last_name, username, password, street_number, street_name, apt_number, postal_code, date_of_birth, country, province, email, phone_number):
    join_date = datetime.today().strftime('%Y-%m-%d')
    self.cursor.execute(f"""INSERT INTO person (username, first_name, middle_name, last_name, password, street_number, street_name, apt_number,
                         postal_code, date_of_birth, country, province) VALUES ('{username}', '{first_name}', '{middle_name}', '{last_name}', '{password}', '{street_number}', '{street_name}', '{apt_number}',
                         '{postal_code}', '{date_of_birth}', '{country}', '{province}')""")
    self.cursor.execute(f"""INSERT INTO users (username, join_date, verified, about, languages, work, profile_picture) VALUES ('{username}', '{join_date}', 'false', 'about me', 'English', 'null', 'default.png')""")
    self.cursor.execute(f"insert into person_phone_number (username, phone_number) VALUES ('{username}', '{phone_number}')")
    self.cursor.execute(f"insert into person_email_address (username, email_address) VALUES ('{username}', '{email}')")

connection = new_connection(dbname = "kpink074", user = "kpink074", password = os.environ.get("UOTTAWA_PW"), host = "web0.site.uottawa.ca", port = "15432", schema = "project")
db = DB(connection)



