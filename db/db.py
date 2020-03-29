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
  
  def get_username_from_id(self, username):
    self.cursor.execute(f"select ID from person where username='{username}'")
  
  def get_password_from_username(self, username):
    self.cursor.execute(f"select password from person where username='{username}'")

  def create_user(self, first_name, middle_name, last_name, username, password, street_number, street_name, apt_number, postal_code, date_of_birth, country, province):
    ID = secrets.token_hex(10)
    join_date = datetime.today().strftime('%Y-%m-%d')
    self.cursor.execute(f"""INSERT INTO person (ID, first_name, middle_name, last_name, username, password, street_number, street_name, apt_number,
                         postal_code, date_of_birth, country, province) VALUES ('{ID}', '{first_name}', '{middle_name}', '{last_name}', '{username}', '{password}', '{street_number}', '{street_name}', '{apt_number}',
                         '{postal_code}', '{date_of_birth}', '{country}', '{province}')""")
    self.cursor.execute(f"""INSERT INTO users (ID, join_date, verified, about, languages, work, profile_picture) VALUES ('{ID}', '{join_date}', 'false', 'about me', 'English', 'null', 'null')""")

connection = new_connection(dbname = "kpink074", user = "kpink074", password = os.environ.get("UOTTAWA_PW"), host = "web0.site.uottawa.ca", port = "15432", schema = "project")
db = DB(connection)



