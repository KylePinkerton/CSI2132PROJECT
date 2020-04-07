from dbconnection import new_connection
import os
import secrets
from datetime import datetime

#change these credentials to change db
dbname = "kpink074"
user = "kpink074"
password = os.environ.get("UOTTAWA_PW")
host = "web0.site.uottawa.ca"
port = "15432"
schema = "project"

class DB:
  def __init__(self, dbname, user, password, host, port, schema):
    self.dbname = dbname
    self.user = user
    self.password = password
    self.host = host
    self.port = port
    self.schema = schema

  def new_connection(self):
    connection = new_connection(self.dbname, self.user, self.password, self.host, self.port, self.schema)
    self.connection = connection
    self.cursor = self.connection.cursor

  def close(self):
    self.connection.close()
  
  #basic db stuff
  def fetch_all(self):
    return self.cursor.fetchall()
  
  def fetch_one(self):
    return self.cursor.fetchone()

  def commit(self):
    self.connection.commit()

  #person
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

  #raw query
  def raw_query(self, query):
    self.cursor.execute(query)

  #admin
  def check_admin(self, username):
    self.cursor.execute(f"select count(username) from admins where username='{username}'")

  #employee
  def check_employee(self, username):
    self.cursor.execute(f"select count(username) from employees where username='{username}'")
  
  def get_title(self, username):
    self.cursor.execute(f" select title from employees where username='{username}' ")

  def get_manager(self, username):
    self.cursor.execute(f" select managerusername from employees where username='{username}' ")

  def get_assigned_properties(self, username):
    self.cursor.execute(f""" select P.propertyname, P.street_name, P.street_number, P.postal_code, P.province, P.country from works_at as W, property as P where W.propertyname=P.propertyname and W.employeeusername='{username}' """)

  def view_employees(self, country):
    self.cursor.execute(f""" select * from employees where country='{country}' """)

  #person
  def valid_username(self, username):
    self.cursor.execute(f"select count(username) from person where username='{username}'")

  def select_from_person(self, username, field):
    self.cursor.execute(f"select {field} from person where username='{username}'")
  
  def select_from_person_email(self, username):
    self.cursor.execute(f"select email_address from person_email_address where username='{username}'")

  def select_from_person_phone(self, username):
    self.cursor.execute(f"select phone_number from person_phone_number where username='{username}'")
  
  def insert_email(self, username, email):
    self.cursor.execute(f"insert into person_email_address (username, email_address) VALUES ('{username}', '{email}')")
  
  def insert_phone_number(self, username, phone_number):
    self.cursor.execute(f"insert into person_phone_number (username, phone_number) VALUES ('{username}', '{phone_number}')")
  
  def update_phone_number(self, username, phone_number):
    self.cursor.execute(f"UPDATE person_phone_number SET phone_number = '{phone_number}' WHERE username = '{username}'")

  def update_picture(self, username, picture):
    self.cursor.execute(f"update users set profile_picture = '{picture}' WHERE username='{username}'")
  
  def get_password_from_username(self, username):
    self.cursor.execute(f"select password from person where username='{username}'")

  def get_country_from_username(self, username):
    self.cursor.execute(f"select country from person where username='{username}'")

  def create_user(self, first_name, middle_name, last_name, username, password, street_number, street_name, apt_number, postal_code, date_of_birth, country, province, email, phone_number):
    join_date = datetime.today().strftime('%Y-%m-%d')
    self.cursor.execute(f"""INSERT INTO person (username, first_name, middle_name, last_name, password, street_number, street_name, apt_number,
                         postal_code, date_of_birth, country, province) VALUES ('{username}', '{first_name}', '{middle_name}', '{last_name}', '{password}', '{street_number}', '{street_name}', '{apt_number}',
                         '{postal_code}', '{date_of_birth}', '{country}', '{province}')""")
    self.cursor.execute(f"""INSERT INTO users (username, join_date, verified, about, languages, work, profile_picture) VALUES ('{username}', '{join_date}', 'false', 'N/A', 'English', 'N/A', 'default.png')""")
    self.cursor.execute(f"insert into person_phone_number (username, phone_number) VALUES ('{username}', '{phone_number}')")
    self.cursor.execute(f"insert into person_email_address (username, email_address) VALUES ('{username}', '{email}')")
  
  #users
  def get_user(self, username):
    self.cursor.execute(f"select * from users where username='{username}'")

  def get_total_users(self):
    self.cursor.execute(f"select count(username) from users where username=username")

  def get_join_date(self, username):
    self.cursor.execute(f"select join_date from users where username='{username}'")
  
  def get_verified(self, username):
    self.cursor.execute(f"select verified from users where username='{username}'")

  def get_about(self, username):
    self.cursor.execute(f"select about from users where username='{username}'")

  def get_languages(self, username):
    self.cursor.execute(f"select languages from users where username='{username}'")
  
  def get_work(self, username):
    self.cursor.execute(f"select work from users where username='{username}'")
  
  def get_picture(self, username):
    self.cursor.execute(f"select profile_picture from users where username='{username}'")

  def update_verified(self, username):
    self.cursor.execute(f"update users set verified='True' where username='{username}'")

  def update_work(self, username, work):
    self.cursor.execute(f"update users set work='{work}' where username='{username}'")
  
  def update_about(self, username, about):
    self.cursor.execute(f"update users set about='{about}' where username='{username}'")

  def update_languages(self, username, languages):
    self.cursor.execute(f"update users set languages='{languages}' where username='{username}'")
  
  #property
  def get_homepage_properties(self):
      self.cursor.execute(f"select * from property order by random() limit 20")

  def get_total_properties(self):
    self.cursor.execute(f"select count(propertyname) from property where propertyname=propertyname")

  def get_property(self, propertyname):
      self.cursor.execute(f"select * from property where propertyname='{propertyname}'")

  def get_users_properties(self, username):
      self.cursor.execute(f"select * from property where hostusername='{username}'")
  
  def valid_propertyname(self, propertyname):
    self.cursor.execute(f"select count(propertyname) from property where propertyname='{propertyname}'")

  def create_property(self, property_name, street_number, street_name, apt_number, postal_code, rent_rate, country, province, property_type, max_guests, number_beds, number_baths, accessible, pets_allowed, current_user_id, picture):
    self.cursor.execute(f"insert into property (propertyname, street_number, street_name, apt_number, province, postal_code, rent_rate, property_type, max_guests, number_beds, number_baths, accessible, pets_allowed, country, hostusername, picture) VALUES ('{property_name}', '{street_number}', '{street_name}', '{apt_number}', '{province}', '{postal_code}', '{rent_rate}', '{property_type}', '{max_guests}', '{number_beds}', '{number_baths}', '{accessible}', '{pets_allowed}', '{country}', '{current_user_id}', '{picture}')")

  def get_search_properties(self, hostusername, propertyname, rent_rate, country, province, property_type, max_guests, number_beds, number_baths, accessible, pets_allowed):
      self.cursor.execute(f"""select * from property where hostusername={hostusername} and propertyname={propertyname} and rent_rate<={rent_rate} and country={country} and province={province} 
      and property_type={property_type} and max_guests>={max_guests} and number_beds>={number_beds} and number_baths>={number_baths} and accessible={accessible} and pets_allowed={pets_allowed} limit 20""")

  #payment_method
  def get_users_payment_methods(self, username):
      self.cursor.execute(f"select * from payment_method where username='{username}'")

  def create_payment_method(self, username, card_type, first_name, last_name, card_number, card_expiration, cvv, billing_country):
    self.cursor.execute(f"insert into payment_method (username, card_type, first_name, last_name, card_number, card_expiration, cvv, billing_country) VALUES ('{username}', '{card_type}', '{first_name}', '{last_name}', '{card_number}', '{card_expiration}', '{cvv}', '{billing_country}')")

  #payout method
  def get_users_payout_methods(self, username):
    self.cursor.execute(f"select * from payout_method where username='{username}'")
  
  def create_payout_method(self, username, paypal_address):
    self.cursor.execute(f"insert into payout_method (username, paypal_address) VALUES ('{username}', '{paypal_address}')")

  #property_taken_dates
  def check_dates(self, propertyname, dates):
    taken_dates = []
    for date in dates:
      date_string = date.strftime('%Y-%m-%d')
      try:
        self.cursor.execute(f"select * from property_taken_dates where propertyname='{propertyname}' and taken_date='{date_string}'")
        if len(self.cursor.fetchall()) == 0:
          continue
        taken_dates.append(date)

      except Exception as e: 
        print(e)
        raise Exception('Something bad happened when checking the dates...')
    
    return taken_dates

  #rental_agreement
  def get_total_completed_stays(self):
    current_date = datetime.today().strftime('%Y-%m-%d')
    self.cursor.execute(f"select count(rental_id) from rental_agreement where host_accepted='true' and end_date<='{current_date}'")

  #branches
  def get_total_countrys(self):
    self.cursor.execute(f"select count(country) from branches where country=country")

  def valid_country(self, country):
    self.cursor.execute(f"select count(country) from person where country='{country}'")
  
db = DB(dbname, user, password, host, port, schema)
db.new_connection()


