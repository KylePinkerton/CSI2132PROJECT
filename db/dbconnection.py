import psycopg2
import os

class DBConnection:
  def __init__(self, dbname, user, password, host, port, schema):
    self.connnection = psycopg2.connect(dbname = dbname, user = user, password = password, host = host, port = port)
    self.cursor = self.connnection.cursor()
    self.schema = schema
    self.cursor.execute(f"SET search_path = {schema}")

def new_connection(dbname = "kpink074", user = "kpink074", password = os.environ.get("UOTTAWA_PW"), host = "web0.site.uottawa.ca", port = "15432", schema = "project"):
  connection = DBConnection(dbname, user, password, host, port, schema)
  return connection