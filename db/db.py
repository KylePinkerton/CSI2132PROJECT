from dbconnection import new_connection
import os

class DB:
  def __init__(self, connection):
    self.connection = connection
    self.cursor = self.connection.cursor
  
  def fetch_all(self):
    return self.cursor.fetchall()

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

  def create_user(self, account_details):
    self.cursor.execute("insert ID, first_name, middle_name, last_name, username, password, count  from artist")

def new_db_instance():
  connection = new_connection(dbname = "kpink074", user = "kpink074", password = os.environ.get("UOTTAWA_PW"), host = "web0.site.uottawa.ca", port = "15432", schema = "project")
  db = DB(connection)
  return db



